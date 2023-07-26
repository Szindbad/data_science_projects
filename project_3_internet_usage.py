import change as change
import pandas as pd

internet = pd.read_csv('internet.csv')

internet.head()

internet = internet.rename({'internet_users_per_100': 'percent_online'}, axis=1)

internet.info()


def amount(row):
    if row['percent_online'] == 0:

        return 'none'

    elif row['percent_online'] < 25:

        return 'few'

    elif row['percent_online'] > 50:

        return 'most'

    else:

        return 'some'


internet['amount'] = internet.apply(amount, axis=1)

internet.tail()

years = pd.pivot_table(internet, values='year', index=['entity', 'code'], columns='amount', aggfunc='min').reset_index()

years.head()

years['few2some'] = years['some'] - years['few']

years['some2most'] = years['most'] - years['some']

print(years['few2some'].mean())

print(years['some2most'].mean())

years[years['code'] == 'CAT'].sort_values('few2some', ascending=True)

internet = internet[internet['year'] > 1999]

internet.head()


def decader(row):
    decade = str(row['year'])

    decade = decade[0:3] + '0s'

    return decade


internet['decade'] = internet.apply(decader, axis=1)

internet.head()

internet.sort_values('year', ascending=True)

internet.head()

decade_growth = internet.groupby(['entity', 'decade']).agg(
    {'percent_online': change, 'year': ['min', 'max']}).reset_index()

decade_growth.head()

decade_growth.columns = ['entity', 'decade', 'change', 'min', 'max']

decade_growth.head()

decade_growth['annual'] = decade_growth['change'] / (decade_growth['max']) - (decade_growth['min'])

decade_growth.head()

decade_growth = pd.pivot_table(decade_growth, values='annual', index='entity', columns='decade')

decade_growth.head()

decade_growth['ratio'] = decade_growth['2010s'] / decade_growth['2000s']

decade_growth.head()

decade_growth['ratio'].describe()
