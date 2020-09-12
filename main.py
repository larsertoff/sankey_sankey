import pandas as pd
import os
import colorama
import random
import plotly

colors = list(vars(colorama.Fore).values())
colorama.init()


def color_randomizer(text) -> str:
    colors = list(vars(colorama.Fore).values())
    five_colors = random.sample(colors, 5)
    colored_chars = [random.choice(five_colors) + char for char in text]
    x = ''.join(colored_chars)
    return x

# Sneaky to ensure it works with ps
print(color_randomizer('Input file name in the data folder either .csv or .xlsx: '))
x = input()

try:
    if 'csv' in x:
        df = pd.read_csv(os.path.join('data', x))
    elif 'xlsx' in x:
        df = pd.read_excel(os.path.join('data', x))
    else:
        df = pd.read_csv(os.path.join('data', 'example_data.csv'))
except:
    raise ValueError(color_randomizer('You are fucked...'))
# Preprocess

df = df.assign(lvl1 = 'stop_1', lvl2 = 'stop_2', lvl3 = 'stop_3', lvl4 = 'stop_4', lvl5 = 'stop_5')
df.columns = df.columns.str.lower()


print(color_randomizer('This is your dataframe: '))
print(df.head())
print(color_randomizer("Now lets make it into a Sankey Plot"))

# Made it now so it does not stop makes more sense maybe?
for tup in df.itertuples():
    i = tup.Index
    string_to_split = tup.comb
    list_of_v = string_to_split.split('_')
    for j in range(len(list_of_v)):
        if j > 4:
            break
        df.loc[i, 'lvl'+str(j+1)] = str(list_of_v[j])+ '_' + str(j+1)

def generate_sankey(df, cat_columns=[], value_cols='', title='Sankey Diagram', colors = ['#9b5de5','#f15bb5','#fee440','#00bbf9','#00f5d4']):
    label_list = []
    color_list = []
    for cat_col in cat_columns:
        label_list_temp = list(set(df[cat_col].values))
        color_list.append(len(label_list_temp))
        label_list = label_list + label_list_temp
        
    label_list = list(dict.fromkeys(label_list))

    color_list_2 = []
    for i, color_n in enumerate(color_list):
        color_list_2 = color_list_2 + [colors[i]]*color_n
        
    for i in range(len(cat_columns)-1):
        if i==0:
            source_df = df[[cat_columns[i],cat_columns[i+1], value_cols]]
            source_df.columns = ['source','target','count']
        else:
            temp_df = df[[cat_columns[i], cat_columns[i+1], value_cols]]
            temp_df.columns = ['source','target','count']
            source_df = pd.concat([source_df,temp_df])
        source_df = source_df.groupby(['source','target']).agg({'count':'sum'}).reset_index()
        
    source_df['sourceID'] = source_df['source'].apply(lambda x: label_list.index(x))
    source_df['targetID'] = source_df['target'].apply(lambda x: label_list.index(x))
    
    data = dict(
        type='sankey',
        node = dict(
          pad = 15,
          thickness = 20,
          line = dict(
            color = "black",
            width = 0.5
          ),
          label = label_list,
          color = color_list_2
        ),
        link = dict(
          source = source_df['sourceID'],
          target = source_df['targetID'],
          value = source_df['count']
        )
      )
    
    layout =  dict(
        title = title,
        font = dict(
          size = 10
        )
    )
       
    fig = dict(data=[data], layout=layout)
    return fig

fig = generate_sankey(df, cat_columns=['lvl1','lvl2', 'lvl3', 'lvl4', 'lvl5'], value_cols='count', title='Sankey Diagram')

plotly.offline.plot(fig, validate=True)

print(color_randomizer('Success!!!!!!!!!!!!!!!!!!'))



