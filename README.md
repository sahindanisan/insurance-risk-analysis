Sigorta Masrafı Tahminleme ve Risk Analizi 
Proje Hakkında
Bu proje, istatistiksel modelleme ve makine öğrenmesi teknikleri kullanılarak bir sağlık sigortası şirketinin müşterilerine ait yıllık sağlık masraflarının tahmin edilmesini amaçlamaktadır. Projede, bireylerin demografik ve fiziksel özellikleri kullanılarak aktüeryal bir fiyatlandırma modeli (risk denklemi) oluşturulmuştur.

Veri Seti
Kaggle'dan alınan insurance.csv veri seti kullanılmıştır. Veri seti 1338 müşteri kaydı ve 7 değişkenden oluşmaktadır:
•	age: Yaş
•	sex: Cinsiyet
•	bmi: Vücut Kitle İndeksi (Boy/Kilo oranı)
•	children: Sahip olunan çocuk/bakmakla yükümlü olunan kişi sayısı
•	smoker: Sigara kullanımı
•	region: ABD içinde yaşanılan coğrafi bölge
•	charges: Sigorta şirketine fatura edilen yıllık sağlık masrafı (Hedef Değişken)
Kullanılan Teknolojiler ve Kütüphaneler
•	Python 3
•	Pandas: Veri manipülasyonu, temizleme ve One-Hot Encoding işlemleri
•	Statsmodels: Çoklu Doğrusal Regresyon (Multiple Linear Regression) modelinin kurulması, p-değerlerinin ve katsayıların analizi

Geliştirme Süreci ve Model Optimizasyonu
1. Veri Hazırlığı (One-Hot Encoding): Metin formatındaki kategorik değişkenler (sex, smoker, region), istatistiksel modelin anlayabilmesi için Pandas get_dummies fonksiyonu ile sayısallaştırıldı. Çoklu bağlantı (Multicollinearity) sorununu önlemek için drop_first=True parametresi kullanılarak "Kukla Değişken Tuzağı" önlendi.
2. İlk Modelin Kurulması: Tüm değişkenler kullanılarak ilk OLS (Sıradan En Küçük Kareler) modeli kuruldu.
3. Model Optimizasyonu (Backward Elimination): İlk modelin p-değerleri (P>|t|) incelendiğinde; Cinsiyet ve yaşanılan coğrafi bölge değişkenlerinin masraflar üzerinde istatistiksel olarak anlamlı bir etkisi olmadığı (p > 0.05) tespit edildi. Modeli matematiksel "gürültülerden" arındırmak için Geriye Doğru Eleme yöntemi uygulandı. Cinsiyet ve bölgeler modelden çıkarılarak model sadece gerçek risk faktörleriyle yeniden eğitildi.
Sonuçlar
Gürültülerden arındırılmış nihai modelin sonuçları şöyledir:
•	R-squared (Açıklanan Varyans): %75.0 (0.750)
•	Modelde kalan tüm değişkenlerin (Yaş, BMI, Çocuk Sayısı, Sigara) p-değerleri 0.001'in altındadır.
İnsan biyolojisi ve anlık kazalar gibi veri setinde bulunmayan dış faktörlerin karmaşıklığı göz önüne alındığında, sadece 4 temel değişken kullanılarak sağlık masraflarının %75 oranında doğru açıklanabilmesi, bu modelin aktüeryal fiyatlandırmada oldukça güçlü ve kullanılabilir olduğunu kanıtlamaktadır.
Fiyatlandırma Denklemi:
Yeni bir müşterinin sağlık masrafını hesaplamak için modelin çıkardığı katsayılar (coef) şu şekildedir: Tahmini Masraf = -12100 + (257.85 * Yaş) + (321.85 * BMI) + (473.50 * Çocuk) + (23810 * Sigara İçiyorsa)
(Not: Sigara içen bir müşterinin diğer şartlar sabitken şirkete çıkardığı ek masraf yaklaşık 23.810 Dolar olarak tespit edilmiştir. Bu durum, fiyatlandırma politikasındaki en büyük kaldıraç noktasıdır.)
