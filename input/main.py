import mariadb
import sys
import csv

# Connect to MariaDB
try:
    conn = mariadb.connect(
        user="root",
        password="example",
        host="host.docker.internal",
        port=3306,
        database="verhalenbank_omeka"
    )
    print('db connected. ok!')
except mariadb.Error as e:
    print(f"Error connecting to MariaDB Platform: {e}")
    sys.exit(1)

# get cursor to db
cur = conn.cursor()

# get all column titles
cur.execute(
    "select DISTINCT(`omeka_elements`.name) as element_name from `omeka_element_texts` left outer join omeka_elements on omeka_element_texts.element_id = omeka_elements.id where record_id in ( SELECT record_id FROM `omeka_element_texts` WHERE `text` = ? and record_type = ?);",
    ('broodjeaapverhaal', 'Item')
)
columns = cur.fetchall()
columns = [column[0] for column in columns]
columns.insert(0, 'Record ID')

# create the output csv file
f = open("/output/output.csv", 'w')
w = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)

# write the column names
w.writerow(columns)

# get all ids
print("getting all ids")
cur.execute(
    "SELECT record_id FROM `omeka_element_texts` where element_id=? and text=? and record_type=?;",
    (58, 'broodjeaapverhaal', 'Item')
)
ids = cur.fetchall()
ids = [i[0] for i in ids]
print(f'number of ids: [{len(ids)}]')

# get all elements
print("getting all elements with record_id")
recordSqlString = "SELECT `omeka_element_texts`.record_id, `omeka_elements`.name as element_name, `omeka_element_texts`.text from `omeka_element_texts` left outer join omeka_elements on omeka_element_texts.element_id = omeka_elements.id where record_id in (SELECT record_id FROM `omeka_element_texts` where element_id=? and text=? and record_type=?);"
cur.execute(
    recordSqlString,
    (58, 'broodjeaapverhaal', 'Item')
)
print('fetching all the element from db')
elements = cur.fetchall()
elements = list(elements)
print(f'number of elements: {len(elements)}')

# convert to dict of list of tuple
results = dict()
for element in elements:
    if element[0] in results.keys():
        results[element[0]][element[1]] = element[2]
    else:
        results[element[0]] = {element[1]: element[2]}
print(f'number of keys {len(results.keys())}')
print('done')

# get row from dict and put into csv
for recordId in results.keys():
    print(f'converting record {recordId}')
    row = list()
    record = results[recordId]
    for c in columns:
        if c in record.keys():
            row.append(record[c])
        else:
            row.append('')
    row[0] = recordId
    print(f'writing record to csv: {row}')
    w.writerow(row)
    print(f'finished record {recordId}')

f.close()
