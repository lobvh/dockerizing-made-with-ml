<h1 align="center">
 Dockerizing madewithml.com Data Engineering task
</h1> 

<p align="center">
<img src = 'https://miro.medium.com/v2/resize:fit:1400/format:webp/1*Cono6sgRNu7N5wF8J67fJg.png' width='800' height='400'> 
</p>

 This is the first 'serious' DE project, where I've tried to Dockerize the whole ELT process presented here:
 https://madewithml.com/courses/mlops/data-stack/
 
 The process is meant to be orchestrated locally, but I wanted to take a challenge and do something that would imitate the real-world scenario.

Here is a [Medium](https://medium.com/@goran.dijak/dockerizing-madewithml-com-data-engineering-project-part-1-dbt-and-airflow-using-astro-cli-d9da506e2efb) article where you can read about the problems I've encountered whilst doing the project. There, I've mainly explained about the `dbt` and `Airflow` part, but here I will present the directory structure and fill in the blanks (setting up `Great Expectations` and `Airbyte`). 

---

First of all, let's start by saying that the easiest way to use pre-configured, lightweight `Airflow` is via `AstroCLI`. I've already tried using official `Airflow` Docker image, but got some wierd errors. Luckily, I've found the `AstroCLI`. I use `macOS` and the first thing I did is `brew install astro`. 

After that I've created the Python virtual environment where in the `requirements.txt` I've put `great_expectations`, `dbt-core` and `black`, then activated the environment.

**NOTE:** Somehow, on my machine, I got some errors while using `Great Expectations` that required me to install `black` dependency, but you can test and see if it works without it!

Run `Docker Desktop`. 

Make a directory for your project, name it whatever you want (I will name it `astro-project`), and then `cd` inside it. In the terminal type in `astro dev init`. It will create `Astro` kind of repository inside. 

>>> `AIRBYTE`

Make sure that when you initialize your GCP project you select resource location to `US`. Somehow I got problems when setting it to `EU` and latter trying to get it working in `dbt Cloud`. 

>>> `GREAT EXPECTATIONS`

Inside your project directory there would be a diretory named `dags`. `cd` inside it and run `great_expectations init` (**NOTE:** You should activate the Python environment we've created above for this to work!). For the rest, follow the [tutorial](https://madewithml.com/courses/mlops/orchestration/). 

>>> `DBT`

To initialize your `dbt` project locally it is pretty much straightforward, and I will skip it here. You can follow the [tutorial](https://madewithml.com/courses/mlops/orchestration/).  One thing that you might have problem with is the `SQL` syntax which looked *smelly* to me when I first read the tutorial. I've provided the proper syntax for `.sql` file inside `/astro-project/dbt/data_warehouse_v1/models/labeled_projects`. 

**P.S.** If you are trying to follow the `dbt Cloud` portion of tutorial you will also have to fix the `SQL` syntax part, but I will leave it up to you to fix it, since `SQL` is **the** essential knowledge you need to have. ;) 

Inside the `astro-project` directory, apart from other directories and files I've additionally created and modified:

1. `dbt` directory which I've mounted and later used to access the `dbt` model as a part of 'imitating' how local `dbt-core` access models. You will understand why I've done this, if you follow up the Medium article I've posted, 
2. `gcp-account` directory where I've put my GCP Service Account JSON file. Not safe, but it is meant to work only on my PC, 
3. `requirements.txt` where I had to include all the necesssary dependencies for the `Airflow` operators to run, 
4. `dbt-requirements.txt` where I've included all the requirements for making `dbt` inside container accessing my `BigQuery` data warehouse, as well as some dependencies like `pytz` which were neccessary since I had few failed `Airflow` DAG triggers. By reading the `Airflow` log file I found out what is missing, 
5. `Dockerfile` and `docker-compose.override.yml` -> Modify them to the ones I've included here. See bellow the explanation. 

>>> `Dockerfile`

I've already explained it in my Medium article, but as `dbt` locally needs you to provide the `GOOGLE_APPLICATION_CREDENTIALS` environmental variable, I had to set it inside the container too. 

>>> `docker-compose.override.yml`

Basically, I've mounted some directories such that each part of the `Airflow` could access it with proper permissions defined.  

---

I've provided here the `Airflow` DAG workflow file (`elt-workflow.py`). Before proceeding, don't forget to change `XXXXX-XXXXX-XXXXX-XXXXX.json` inside each of the files I've provided you with the proper GCP Service Account `JSON` file name you've obtained. 

After you've copied all the necessary files from `astro-project` provided here into your `project-name` directory, don't forget to `cd` into your `project-name` directory and run `astro dev start`. After that, in the next terminal tab `cd` into your `Airbyte` folder and do `docker-compose up`.

Now, everything should be set up! Type in your browser `localhost:8080` and trigger the DAG!
