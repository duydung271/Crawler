import json

data = []

for i in '123456':
    f = open('data'+i+'.json',encoding = 'utf-8-sig')
    data1 = json.load(f)
    f.close()
    for d in data1:
        data.append(d)

with open('data.json', 'w') as f:
    json.dump(data, f)

print(len(data))