# вывод ученых и их тем с условиями(из json с замененной должнностью на ученую степень)

BASE_URL = 'https://rinh-api.kovalev.team'
departament = requests.get(f"{BASE_URL}/department/info").json()
istitute = requests.get(f"{BASE_URL}/institute").json()
employee = requests.get(f"{BASE_URL}/employee").json()
poss = requests.get(f"{BASE_URL}/academic/degree").json()

# Добавляем институты в департаменты

# Создаем словарь с институтами и их id
institute_dict = {}
for i in istitute:
    institute_dict[i["id"]] = i["name"]

# Создаем пустой список
deps = []

# Проходим по каждому элементу исходного списка "department"
for d in departament:
    # Создаем новый словарь
    new_dict = {}
    # Заполняем его полями "id", "namedepartment" и "nameinstitute"
    new_dict["id"] = d["departments"]["id"]
    new_dict["namedepartment"] = d["departments"]["name"]
    new_dict["nameinstitute"] = institute_dict[d["departments"]["instituteId"]]
    # Добавляем созданный словарь в список
    deps.append(new_dict)

# Добавляем департаменты и институты в ученых

result = []

for emp in employee:
    for dep in deps:
        if emp['departmentId'] == dep['id']:
            new_dict = {}
            new_dict['id'] = emp['id']
            new_dict['fullName'] = emp['fullName']
            new_dict['academicDegreeId'] = emp['academicDegreeId']
            new_dict['email'] = emp['email']
            new_dict['phone'] = emp['phone']
            new_dict['wosAuthorId'] = emp['wosAuthorId']
            new_dict['namedepartment'] = dep['namedepartment']
            new_dict['nameinstitute'] = dep['nameinstitute']
            result.append(new_dict)
            break

# Добавляем веса и должности в ученых

itog = []

for uch in result:
    for it in poss:
        if uch['academicDegreeId'] == it['id']:
            new_di = {}
            new_di['id'] = uch['id']
            new_di['fullName'] = uch['fullName']
            new_di['email'] = uch['email']
            new_di['phone'] = uch['phone']
            new_di['wosAuthorId'] = uch['wosAuthorId']
            new_di['namedepartment'] = uch['namedepartment']
            new_di['nameinstitute'] = uch['nameinstitute']
            new_di['namedeg'] = it['fullName']
            new_di['weightdeg'] = it['weight']
            itog.append(new_di)
            break

# выписываем все id ученых
BASE_URL7 = 'https://rinh-api.kovalev.team'
response3 = requests.get(f"{BASE_URL7}/employee").json()
id_users = []
for name2 in response3:
    id_users.append(name2["id"])

BASE_URL8 = 'https://rinh-api.kovalev.team/publication/employee/article/info/'

for id_id in id_users:
    data33 = requests.get(f"{BASE_URL8}{id_id}/keywords")
    if len(data33.text) != 0:
        data_sorted = sorted(data33.json(), key=lambda x: x["countArticle"], reverse=True)
        data_sorted_20 = data_sorted[:20]
        for item in itog:
            if item["id"] == id_id:
                item["20words"] = data_sorted_20

                # вывод всех данных
# print(itog)


# вывод только фио и ключевых слов
# for item in itog:
#    print(item['fullName'], item.get('20words', []))

print("Введите тему")
kluch = str(input())
print("Введите департамент")
depps = str(input())
print("Введите должность")
posis = str(input())
filtered_data = []
for item in itog:
    if depps in item['namedepartment'] and posis in item['namedeg'] and '20words' in item:
        for word in item['20words']:
            if kluch in word['keyword']:
                filtered_data.append({
                    'fullName': item['fullName'],
                    'keyword': word['keyword'],
                    'countArticle': word['countArticle']
                })

# print(filtered_data)

top_keywords = [x["countArticle"] for x in filtered_data]
top_counts = [x["fullName"] for x in filtered_data]

# Построение столбчатой диаграммы
fig, ax = plt.subplots(figsize=(16, 6))
plt.bar(top_counts, top_keywords)
plt.xticks(rotation=45, ha='right')
plt.xlabel("Ученые")
plt.ylabel("Количество статей")
plt.title(f"Ученые из департамента: {depps} связанные с {kluch}")
plt.show()