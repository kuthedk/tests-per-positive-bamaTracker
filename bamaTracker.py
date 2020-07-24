import json
import requests
import matplotlib.pyplot as plt

daily_tests_ran = []
daily_case_increase = []
dates = []

county = input("Enter name of county or enter 'state' to get the entire state. \n ").lower()

print(county)

if county == "state":
    response = requests.get('https://bamatracker.com/api/daily')
    plt.suptitle("Test Per Positive for Alabama")
elif county == '':
    response = requests.get('https://bamatracker.com/api/daily/Madison')
    plt.suptitle("Test Per Positive for Madison County Alabama")
else:
    response = requests.get('https://bamatracker.com/api/daily/' + county)
    plt.suptitle("Test Per Positive for " + county.capitalize() + " County Alabama")
if response.status_code != 200:
    print(str(response.status_code))
else:
    print("Success")
    json_data = json.loads(response.text)
    print(json_data)
    x = 0
    for i in range(len(json_data)):
        if x > 0:
            daily_case_increase.append(json_data[i]["cases"] - json_data[i - 1]["cases"])
            daily_tests_ran.append(json_data[i]['tested'] - json_data[i - 1]['tested'])
        else:
            daily_case_increase.append(json_data[i]["cases"])
            daily_tests_ran.append(json_data[i]["tested"])
        dates.append(json_data[i]["date"].replace("2020-", ""))
        x += 1

test_per_positive = []
tpp_dates = []

for i in range(len(daily_case_increase)):
    if daily_tests_ran[i] != 0 and daily_case_increase[i] > 0:
        test_per_positive.append(daily_tests_ran[i] / daily_case_increase[i])
    else:
        test_per_positive.append(0)
    tpp_dates.append(dates[i])

x = tpp_dates[-21:]
y = test_per_positive[-21:]
y7da = []
y3da = []
y14da = []
for date in x:
    sda = []
    tda = []
    fda = []
    for i in range(6, -1, -1):
        sda.append(test_per_positive[tpp_dates.index(date) - i])
    for i in range(2, -1, -1):
        tda.append(test_per_positive[tpp_dates.index(date) - i])
    for i in range(13, -1, -1):
        fda.append(test_per_positive[tpp_dates.index(date) - i])
    y7da.append(sum(sda) / len(sda))
    y3da.append(sum(tda) / len(tda))
    y14da.append(sum(fda) / len(fda))

plt.bar(x, y, color='#018571')
plt.plot(x, y3da, marker='o', linestyle="--", color='#a6611a', label="3 day average")
plt.plot(x, y7da, marker='o', linestyle="--", color='#dfc27d', label="7 day average")
plt.plot(x, y14da, marker='o', linestyle="--", color='#80cdc1', label="14 day average")
plt.xticks(rotation=90)
plt.title(
    "How many tests does it take to find 1 positive case? More testing with fewer positive cases is assumed to be an indication of progress. ",
    wrap=True,
    size=8)
plt.grid()
plt.xlabel("Dates in 2020\n Data from https://www.bamatracker.com")
plt.ylabel("Test per positive")
plt.subplots_adjust(bottom=0.20)
plt.legend()
plt.show()
