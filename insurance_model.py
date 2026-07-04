import pandas as pd
import statsmodels.api as sm
import seaborn as sns
import matplotlib.pyplot as plt
# Tüm 7 değişkeni (age, sex, bmi, children, smoker, region, charges) içeren tabloyu okuyoruz.
df = pd.read_csv("insurance.csv")

#  VERİ GÖRSELLEŞTİRME 
# BMI ve Sigara kullanımının masraflar üzerindeki etkisini görselleştiriyoruz
plt.figure(figsize=(10, 6))
sns.scatterplot(x='bmi', y='charges', hue='smoker', data=df)
plt.title('Vücut Kitle İndeksi (BMI) ve Sigara Kullanımının Sağlık Masraflarına Etkisi')
plt.xlabel('Vücut Kitle İndeksi (BMI)')
plt.ylabel('Yıllık Sağlık Masrafı ($)')
plt.show()

# VERİ TEMİZLEME VE DÖNÜŞTÜRME
# Sayısal değerler aynen kalırken; cinsiyet, sigara ve bölge metinleri 1 ve 0'lara dönüşür.
df_tam = pd.get_dummies(df, columns=['sex', 'smoker', 'region'], drop_first=True)
# İSTATİSTİKSEL MODELİ HAZIRLAMA (İLK MODEL)
y_tam = df_tam['charges']
X_tam = df_tam.drop('charges', axis=1) # axis=1: İşlemin sütunlar üzerinde yapılacağını belirtir
X_tam = sm.add_constant(X_tam.astype(float))
tam_model = sm.OLS(y_tam, X_tam).fit()
print("\n--- TÜM DEĞİŞKENLERLE İLK MODEL ---")
print(tam_model.summary())

#MODEL OPTİMİZASYONU (BACKWARD ELIMINATION - ADIM 1)
# P değerlerine baktık; cinsiyetin ve kuzeybatıda yaşamanın bir etkisi olmadığını gördük, çıkartıyoruz.
print("\n--- TEMİZLENMİŞ HALİ (ADIM 1) ---")
y_tamd = df_tam['charges']
x_tamd = df_tam.drop(['charges','sex_male','region_northwest'] , axis=1)
x_tamd = sm.add_constant(x_tamd.astype(float))
tam_modeld = sm.OLS(y_tamd , x_tamd).fit()
print(tam_modeld.summary())

#MODEL OPTİMİZASYONU (BACKWARD ELIMINATION - ADIM 2)
# İşlem sonucu region_southwest p değeri 0.05'ten büyük geldiği için onu da siliyoruz.
print("\n--- TEMİZLENMİŞ HALİ (ADIM 2) ---")
y_tamd2 = df_tam['charges']
x_tamd2 = df_tam.drop(['charges','sex_male','region_southwest','region_northwest'] , axis=1)
x_tamd2 = sm.add_constant(x_tamd2.astype(float))
tam_modeld2 = sm.OLS(y_tamd2 , x_tamd2).fit()
print(tam_modeld2.summary())

#MODEL OPTİMİZASYONU (FİNAL MODELİ)
# İşlem sonucu region_southeast p değeri de 0.05'ten büyük geldiği için onu da siliyoruz.
print('\n--- SON TEMİZLENMİŞ HALİ (NİHAİ MODEL) ---')
y_tamd3 = df_tam['charges']
x_tamd3 = df_tam.drop(['charges','sex_male','region_southwest','region_northwest','region_southeast'] , axis=1)
x_tamd3 = sm.add_constant(x_tamd3.astype(float))
tam_modeld3 = sm.OLS(y_tamd3 , x_tamd3).fit()
print(tam_modeld3.summary())

#YENİ MÜŞTERİ TAHMİNİ 
# Gelen müşterinin özellikleri: Sabit(1), Yaş(45), BMI(25.0), Çocuk Sayısı(4), Sigara(Evet=1)
yeni_musteri = [1, 45, 25.0, 4, 1]
tahmini_fatura = tam_modeld3.predict(yeni_musteri)
print(f"\nBu müşterinin tahmini yıllık sağlık masrafı: {tahmini_fatura[0]:.2f} Dolar")
