SELECT p.id, p.created_on, p.title, p.description, t.tag
FROM `dl-project-377619.made_with_ml.projects` AS p
LEFT JOIN `dl-project-377619.made_with_ml.tags` AS t
ON p.id = t.id
