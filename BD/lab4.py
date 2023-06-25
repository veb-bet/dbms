from pymongo import MongoClient


def connect():
    uri = "mongodb://localhost:27017"
    client = MongoClient(uri)
    return client


def get_collection(client, collection_name):
    db = client['diagnosis_db']
    collection = db['diagnosis']
    return collection


def insert_record(collection, record):
    result = collection.insert_one(record)
    print('Добавили запись:', result.inserted_id)


def find_all_records(collection):
    cursor = collection.find()
    for record in cursor:
        print(record)


def delete_record(collection, query):
    result = collection.delete_one(query)
    print('Удалили запись', result.deleted_count)


def update_record(collection, query, update):
    result = collection.update_one(query, update)
    print('Изменили запись', result.modified_count)

if __name__ == '__main__':
    collection_name = 'diagnosis'
    client = connect()
    collection = get_collection(client, collection_name)

    while True:
        action = input('Выберите действие (add, show, delete, update, functional_query, exit): ')

        if action == 'exit':
            break

        elif action == 'add':
            record = {
                '_id': input('Введите id заболевания: '),
                'articles.author': input('Введите автора статьи: '),
                'articles.heading': input('Введите заголовок статьи: '),
                'articles.link': input('Введите ссылку на статью: '),
                'articles.publicationDate': input('Введите дату публикации статьи (YYYY-MM-DD): '),
                'medication.medicine': input('Введите название лекарства: '),
                'medication.type': input('Введите тип лекарства: '),
                'method.nameMethod': input('Введите название метода лечения: '),
                'method.therapy': input('Введите описание метода лечения: '),
                'name': input('Введите название заболевания: '),
            }
            insert_record(collection, record)

        elif action == 'show':
            find_all_records(collection)

        elif action == 'delete':
            query = {'_id': input('Введите id записи, которую необходимо удалить: ')}
            delete_record(collection, query)

        elif action == 'update':
            query = {'_id': input('Введите id записи, которую необходимо обновить: ')}
            update_query = {'$set': {input('Введите поле, которое необходимо обновить: '): input('Введите новое значение: ')}}
            update_record(collection, query, update_query)

        elif action == 'functional_query':
            functional_query_number = input('Выберите функциональный запрос (1, 2): ')

            if functional_query_number == '1':
                query = {'articles.publicationDate': {'$gt': '2022-01-01'}}
                cursor = collection.find(query)
                for record in cursor:
                    print(record)

            elif functional_query_number == '2':
                query = {'articles.publicationDate': {'$gt': '2022-01-01'}}
                projection = {'method.therapy': 1, 'name': 1, '_id': 0}
                cursor = collection.find(query, projection)
                for record in cursor:
                    print(record)

            else:
                print('Неизвестный функциональный запрос')

        else:
            print('Неизвестное действие')

    client.close()
