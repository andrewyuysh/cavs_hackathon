import pandas as pd
import matplotlib.pyplot as plt

def df_transactions():
    retail = pd.read_csv(
        '/Users/andrewyuysh/code/cavs_hackathon/hackathon_2425_retail_final(in).csv',
        dtype={
            'transaction_id': 'str',
            'customer_id': 'str',
            'total_amount': 'float',
            'price': 'float',
            'quantity': 'int',
            'subtotal': 'float',
            'tax': 'float',
            'transaction_date': 'str',
            'transaction_time': 'str',
            'transaction_datetime': 'str'
        }
    )
    retail['transaction_datetime'] = pd.to_datetime(retail['transaction_date'].str.replace('0:00','') + ' ' + retail['transaction_time'])
    retail.drop(columns=['transaction_date', 'transaction_time'], inplace=True)

    fnb = pd.read_csv(
        '/Users/andrewyuysh/code/cavs_hackathon/hackathon_2425_fnb_final(in).csv',
        dtype={
            'transaction_id': 'str',
            'customer_id': 'str',
            'total_amount': 'float',
            'price': 'float',
            'quantity': 'int',
            'subtotal': 'float',
            'tax': 'float',
        }
    )
    fnb['transaction_datetime'] = pd.to_datetime(fnb['transaction_date'].str.replace('0:00','') + ' ' + fnb['transaction_time'])
    fnb.drop(columns=['transaction_date', 'transaction_time'], inplace=True)

    fnb['category'] = 'fnb'
    retail['category'] = 'retail'
    df = pd.concat([fnb, retail], ignore_index=True)
    df['date'] = df['transaction_datetime'].dt.date
    df['hour'] = df['transaction_datetime'].dt.hour
    # dates = sorted(df['transaction_datetime'].dt.date.unique())
    return df

def df_games():
    # https://www.nba.com/stats/team/1610612739/boxscores?Season=2023-24&SeasonType=Regular%20Season&dir=D&sort=GDATE
    games = pd.read_csv('games.csv').drop_duplicates('MATCHUP')
    games['DATE'] = pd.to_datetime(games['MATCHUP'].str.split(' - ').str[0])
    games['MATCHUP'] = games['MATCHUP'].str.split(' - ').str[1]
    games = games.sort_values('DATE')
    games['HOME'] = games['MATCHUP'].str.contains('vs')
    # home_games = set(games[games['HOME']]['DATE'].dt.date.to_list())
    # print('home game was played but no transactions:')
    # print(home_games - set(dates))
    # print('transactions were made but no home game was played:')
    # print(set(dates) - home_games)
    return games

C = [
    (134, 0, 56), #'r'
    (0, 0, 0), #'k'
    (27, 47, 103), #'b'
    (188, 148, 92), #'g'
    (227, 82, 5), #'o'
    (92, 136, 218), #'lb'
]
C = [tuple(v / 255 for v in c) for c in C]
plt.rcParams['axes.facecolor'] = C[3]
plt.rcParams['figure.facecolor'] = 'none'

L = ['Superfans', 'Shoppers', 'Regulars']

def item_cat(item):
    if item in ['Nachos', 'Hamburger', 'Pepperoni Pizza', 'Cheese Pizza', 'Cheeseburger', 'Hot Dog']:
        return 'hotfood'
    elif item in ['Cherry Coke', 'Water', 'Coke Zero', 'Diet Coke', 'Coke', 'MinuteMaid Lemonade', 'Sprite']:
        return 'nonalc'
    elif item in ['Bud Light', 'Great Lakes Craft Beer', 'Budweiser']:
        return 'alc'
    elif item in ['Popcorn', 'Ice Cream', 'Sour Patch Kids Box', 'Reeses Pieces Box', 'Swedish Fish Box', 'M&M Box', 'Pretzel']:
        return 'snacks'
    elif item in ['Sweatshirt', 'Shorts', 'Jacket', 'T-Shirt', 'Pants', 'Jersey']:
        return 'clothing'
    elif item in ['Accessories', 'Scarf', 'Hat', 'Socks']:
        return 'accessories'
    else: raise ValueError
