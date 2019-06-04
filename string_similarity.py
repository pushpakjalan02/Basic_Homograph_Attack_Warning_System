import mysql.connector

my_db_connection = mysql.connector.connect(
    host = "localhost",
    user = "localhost",
    passwd = "root",
    database = "url_similarity"
)

pointer = my_db_connection.cursor()

def preprocess_query_result(query_result):
    i = 0
    while i < len(query_result):
        length = len(query_result[i][0])
        query_result[i] = query_result[i][0]
        i += 1

def calculate_jaro_winkler_distance(query_compare_value, search_url):
    alphabet_count_array = [0] * 128
    alphabet_count_array2 = [0] * 128
    for i in query_compare_value:
        alphabet_count_array[ord(i)] += 1;
    for i in search_url:
        alphabet_count_array2[ord(i)] += 1;
    i = 0
    m = 0
    while i < 128:
        m += min(alphabet_count_array[i], alphabet_count_array2[i])    
        i += 1
    modulus_s1 = len(query_compare_value)
    modulus_s2 = len(search_url)
    t = 0
    i = 0
    while i < max(modulus_s1, modulus_s2):
        if i < min(modulus_s1, modulus_s2):
            if query_compare_value[i] == search_url[i]:
                t += 1
        else:
            t += max(modulus_s1, modulus_s2) - i
            break
        i += 1
    t /= 2
    if m != 0:
        jaro_distance = (1/3.0) * ((m/modulus_s1) + (m/modulus_s2) + ((m - t)/m))
    else:
        jaro_distance = (1/3.0) * ((m/modulus_s1) + (m/modulus_s2))
#    if jaro_distance < 0:
#        jaro_distance = 0
    prefix_scale = 0.1
    l = 0
    while l < min(modulus_s1, modulus_s2):
        if query_compare_value[l] != search_url[l]:
            l += 1
            break
        l += 1
    l = min(l,4)
    jaro_winkler_distance = jaro_distance + l * prefix_scale * (1 - jaro_distance)
    return jaro_winkler_distance

def scrap(string_1, string_2):
    if string_1[0:4] == string_2[0:4]:
        string_1 = string_1[4:]
        string_2 = string_2[4:]
    i = len(string_1) - 1
    while i >= 0:
        if string_1[i] == '.':
            break
        i -= 1
    j = len(string_2) - 1
    while j >= 0:
        if string_2[j] == '.':
            break
        j -= 1
    if string_1[i:] == string_2[j:]:
        string_1 = string_1[0:i]
        string_2 = string_2[0:j]
    list_to_compare = []
    list_to_compare.append(string_1)
    list_to_compare.append(string_2)
    return list_to_compare

def execute_jaro_winkler(search_url, threshold, query_result):
#    percentage_similarity = []
    display_list = []
    flag = 0
    for i in query_result:
        list_to_compare = scrap(i, search_url)
        distance_value = calculate_jaro_winkler_distance(list_to_compare[0], list_to_compare[1])
        distance_value *= 100
        if int(distance_value) > threshold:
            display_list.append(i)
            flag = 1
    if flag != 0:
        print('You may have probably meant:')
        for i in display_list:
            print(i)
    else:
        print('No similar URL found.')

def check_string_similarity(search_url):
    pointer.execute("SELECT * from urls;")
    query_result = pointer.fetchall()
    preprocess_query_result(query_result)
    threshold = 67
    execute_jaro_winkler(search_url, threshold, query_result)

def main():
    search_url = input('Enter URL\n')
    check_string_similarity(search_url)

if __name__ == '__main__':
    main()
