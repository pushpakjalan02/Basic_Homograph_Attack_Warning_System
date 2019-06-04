import mysql.connector

def main():
    my_db_connection = mysql.connector.connect(
        host = "localhost",
        user = "localhost",
        passwd = "root",
        database = "url_similarity"
    )
    print(my_db_connection)
    pointer = my_db_connection.cursor()
    print('Enter 0 when done')
    list_to_append = []
    j = 0
    while(True):
        list_to_append.append(input())
        if list_to_append[j] == '0':
            break
        j += 1
    i = 0
    while i < j:
        query = "INSERT INTO urls VALUES ('"+ list_to_append[i] +"');"
        pointer.execute(query)
        my_db_connection.commit()
        i += 1
    print(j, "Record Inserted...")

if __name__ == '__main__':
    main()
