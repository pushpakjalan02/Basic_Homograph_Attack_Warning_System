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
    url = input("Enter URL\n");
    query = "INSERT INTO urls VALUES ('"+ url +"');"
    pointer.execute(query)
    my_db_connection.commit()
    print(pointer.rowcount, "Record Inserted...")

if __name__ == '__main__':
    main()
