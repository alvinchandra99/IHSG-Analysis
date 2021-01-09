import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


st.title('Menakar Kekuatan Investor Retail di Pasar Modal Indonesia')

st.markdown("""
2020 merupakan tahun yang menarik, masyarakat dari berbagai macam kalangan mulai ikut berinvestasi di Pasar Modal. 
Berdasarkan data bursa efek Indonesia (BEI) per 19 November 2020, jumlah investor saham mencapai 1,5 juta atau tumbuh 36,13 persen dari tahun sebelumnya.

Lalu, bagaimana **kekuatan investor retail** di pasar modal Indonesia? 
Apakah investor retail mampu menggerakan IHSG?
""")

st.header("Kategori Investor")
st.markdown(""" Pada umumnya, investor pada Pasar Modal Indonesia dibedakan menjadi dua kelompok, yaitu Investor Lokal dan Investor Asing.
Investor retail merupakan investor perseorangan atau investor individu yang berinvestasi atas nama perorangan.
""")

#st.sidebar.header('User Input Features')

# Web scraping of S&P 500 data
#
@st.cache
def load_data():
    df = pd.read_csv('Balancepos20201230.txt', delimiter='|')
    data = pd.DataFrame(df[df['Type'] == "EQUITY"])
    data['Local Value'] = data['Total'] * data['Price']
    data['Foreign Value'] = data['Total.1'] * data['Price']
    data['Local Non ID Value'] = (data['Total'] - data['Local ID'])*data['Price']
    data['Local ID Value'] = data['Local ID'] * data["Price"]
    
    return data

df = load_data()




st.header('Data Kepemilikan Saham di IHSG')
st.write('Data Dimension: ' + str(df.shape[0]) + ' rows and ' + str(df.shape[1]) + ' columns.')
st.dataframe(df)


st.markdown(""" * Sumber Data : [KSEI](https://www.ksei.co.id/).
* Local =  Investor Lokal
* Foregin = Investor Asing
* Local ID = Investor Individu Lokal / Investor Retail
""")



#Bar Chart
def func(pct, allvals):
    absolute = str((int(pct/100.*np.sum(allvals)))/1000000000000)
    return "{:.1f}%\n({} T)".format(pct, absolute[:7])



sizes = [df.sum()['Local Value'] , df.sum()['Foreign Value']]
labels = ["Local", "Foreign"]

fig1, ax1 = plt.subplots()
ax1.pie(sizes, labels =labels, startangle =90, autopct=lambda pct: func(pct, sizes), shadow = True)
ax1.set_title("Komposisi Investor Lokal vs Asing")
ax1.axis('equal') 


st.pyplot(fig1)

st.write("""
PER 30 Desember 2020, Investor Lokal memiliki porsi sebesar 50.8 persen atau sekitar 1913 Triliun Rupiah dan 
Investor Asing memiliki porsi 49.2 persen atau sekitar 1853 Triliun Rupiah. Lalu untuk investor retail memiliki porsi sebagai berikut

""")
sizes2 = [df.sum()['Local Non ID Value'], df.sum()['Local ID Value'], df.sum()['Foreign Value']]
labels2 = ["Institusi", "Retail", "Asing"]
explode = (0, 0.1,  0) 

fig2, ax2 = plt.subplots()
ax2.pie(sizes2, labels = labels2, startangle = 90, explode = explode, autopct=lambda pct: func(pct, sizes2), shadow = True)
ax2.set_title("Komposisi Investor Retail")
ax2.axis('equal') 

st.pyplot(fig2)
st.write("""
Posisi Investor Retail di IHSG terbilang cukup kecil, hanya sebesar 13 persen dari Market Cap Saham Beredar di IHSG

""")


def line_chart_data() :
    df = pd.read_csv('Balancepos20201230.txt', delimiter='|')
    df2 = pd.read_csv('Balancepos20200630.txt', delimiter='|')
    df3 = pd.read_csv('Balancepos20191230.txt', delimiter='|')
    df4= pd.read_csv('Balancepos20190628.txt', delimiter='|')
    df5 = pd.read_csv('Balancepos20181228.txt', delimiter='|')
    df6 = pd.read_csv('Balancepos20180629.txt', delimiter='|')

    data = pd.DataFrame(df[df['Type'] == "EQUITY"])
    data2 = pd.DataFrame(df2[df2['Type'] == "EQUITY"])
    data3 = pd.DataFrame(df3[df3['Type'] == "EQUITY"])
    data4 = pd.DataFrame(df4[df4['Type'] == "EQUITY"])
    data5 = pd.DataFrame(df5[df5['Type'] == "EQUITY"])
    data6 = pd.DataFrame(df6[df6['Type'] == "EQUITY"])

    member = [data,data2,data3,data4,data5,data6]

    for x in member :
        x['Local Value'] = x['Total'] * x['Price']
        x['Foreign Value'] = x['Total.1'] * x['Price']
        x['Local Non ID Value'] = (x['Total'] - x['Local ID'])*x['Price']
        x['Local ID Value'] = x['Local ID'] * x["Price"]
        x['Total Value'] = x["Local Value"] + x['Foreign Value']
        
    

    LocalID = []

    for x in member:
        LocalID.append((x.sum()['Local ID Value']/x.sum()['Total Value']) * 100)



    hasil = pd.DataFrame.from_dict({'2020-12' : LocalID[0], '2020-06' : LocalID[1], '2019-12' : LocalID[2], '2019-06' : LocalID[3], '2018-12':LocalID[4], '2018-06' : LocalID[5]}, orient='index', columns=['Local ID'])
   

    return hasil
st.markdown("Dari tahun 2018 hingga tahun 2020, persentasi investor retail di IHSG masih terlihat mengalami peningkatan singnifikan.")
st.line_chart(line_chart_data())

st.header('Kesimpulan')
st.markdown("""

* Jumlah investor retail meningkat, akan tetapi nilai saham yang dimiiki hanya meningkat sekitar 1-2% pertahun.
* Investor Retail memiiki kekuatan yang kecil di IHSG, hanya sekitar 13%
* Pergerakan IHSG Masih didominasi oleh Investor Asing dan Investor Institusi Lokal
""")