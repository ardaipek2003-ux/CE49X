import pandas as pd
import io

# 1. Load Building Data (Aggregated from Neighborhoods)
raw_bina_path = 'Week04_Matplotlib_Visualization/lab/data/mahalle-bazli-bina-analiz-verisi.csv'
df_bina_raw = pd.read_csv(raw_bina_path, sep=';', encoding='ISO-8859-9')

# Aggregate by District
agg_cols = {
    '1980_oncesi': 'sum',
    '1980-2000_arasi': 'sum',
    '2000_sonrasi': 'sum'
}
df_bina_agg = df_bina_raw.groupby('ilce_adi').agg(agg_cols).reset_index()
df_bina_agg['Total_Buildings'] = df_bina_agg['1980_oncesi'] + df_bina_agg['1980-2000_arasi'] + df_bina_agg['2000_sonrasi']
df_bina_agg['Pre_2000_Count'] = df_bina_agg['1980_oncesi'] + df_bina_agg['1980-2000_arasi']

# 2. Population Data (Sourced from TUIK 2024 results via search)
pop_data = """District,Population_2024
Esenyurt,988369
Küçükçekmece,789033
Pendik,749356
Ümraniye,727819
Bağcılar,713594
Bahçelievler,560086
Sultangazi,532601
Maltepe,524921
Başakşehir,520467
Üsküdar,512981
Sancaktepe,502077
Gaziosmanpaşa,479931
Kartal,475859
Kadıköy,462189
Kağıthane,444820
Avcılar,440934
Esenler,423625
Eyüpsultan,420706
Beylikdüzü,415290
Ataşehir,414866
Sultanbeyli,369193
Fatih,354472
Arnavutköy,344868
Sarıyer,342582
Çekmeköy,306739
Tuzla,301400
Büyükçekmece,280528
Zeytinburnu,278344
Bayrampaşa,268303
Güngören,264831
Şişli,263063
Beykoz,245440
Silivri,232156
Bakırköy,219893
Beyoğlu,216688
Beşiktaş,167264
Çatalca,80399
Şile,48936
Adalar,16979
"""
df_pop = pd.read_csv(io.StringIO(pop_data))

# 3. Mapping for Merging (IBB names vs TUIK names)
# IBB names in df_bina_agg are ALL CAPS. TUIK names in df_pop are Title Case.
mapping = {
    'ADALAR': 'Adalar',
    'ARNAVUTKÖY': 'Arnavutköy',
    'ATAŞEHİR': 'Ataşehir',
    'AVCILAR': 'Avcılar',
    'BAĞCILAR': 'Bağcılar',
    'BAHÇELİEVLER': 'Bahçelievler',
    'BAKIRKÖY': 'Bakırköy',
    'BAŞAKŞEHİR': 'Başakşehir',
    'BAYRAMPAŞA': 'Bayrampaşa',
    'BEŞİKTAŞ': 'Beşiktaş',
    'BEYKOZ': 'Beykoz',
    'BEYLİKDÜZÜ': 'Beylikdüzü',
    'BEYOĞLU': 'Beyoğlu',
    'BÜYÜKÇEKMECE': 'Büyükçekmece',
    'ÇATALCA': 'Çatalca',
    'ÇEKMEKÖY': 'Çekmeköy',
    'ESENLER': 'Esenler',
    'ESENYURT': 'Esenyurt',
    'EYÜP': 'Eyüpsultan',
    'FATİH': 'Fatih',
    'GAZİOSMANPAŞA': 'Gaziosmanpaşa',
    'GÜNGÖREN': 'Güngören',
    'KADIKÖY': 'Kadıköy',
    'KAĞITHANE': 'Kağıthane',
    'KARTAL': 'Kartal',
    'KÜÇÜKÇEKMECE': 'Küçükçekmece',
    'MALTEPE': 'Maltepe',
    'PENDİK': 'Pendik',
    'SANCAKTEPE': 'Sancaktepe',
    'SARIYER': 'Sarıyer',
    'SİLİVRİ': 'Silivri',
    'SULTANBEYLİ': 'Sultanbeyli',
    'SULTANGAZİ': 'Sultangazi',
    'ŞİLE': 'Şile',
    'ŞİŞLİ': 'Şişli',
    'TUZLA': 'Tuzla',
    'ÜMRANİYE': 'Ümraniye',
    'ÜSKÜDAR': 'Üsküdar',
    'ZEYTİNBURNU': 'Zeytinburnu'
}

df_bina_agg['District'] = df_bina_agg['ilce_adi'].map(mapping)

# 4. Merge
df_merged = pd.merge(df_pop, df_bina_agg[['District', 'Pre_2000_Count', 'Total_Buildings']], on='District', how='left')

# Calculate percentage of pre-2000 buildings
df_merged['Pre_2000_Percentage'] = (df_merged['Pre_2000_Count'] / df_merged['Total_Buildings'] * 100).round(2)

# 5. Save final dataset
output_path = 'Week04_Matplotlib_Visualization/lab/data/istanbul_population_building.csv'
df_merged.to_csv(output_path, index=False)
print(f"Successfully created {output_path} with {len(df_merged)} records.")
