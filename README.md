Homework for course "Highload web-systems"

API:

GET /
Возвращает описание API

GET /place_types
Возвращает список известных типов мест

GET /places
Возвращает описание всех мест

PUT /places
Добавляет объект в коллекцию мест

DELETE /places/<place_id>
Удаляет объект по id

POST /nearest/<type>,<lon>,<lat>
Находит ближайший объект указанного типа к заданным координатам
