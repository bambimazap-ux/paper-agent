# מדריך פריסה לענן (Streamlit Community Cloud) 🚀

מדריך זה מסביר כיצד להעלות את סוכן הורדת המאמרים למאגר GitHub משלכם ולפרוס אותו בחינם לענן של Streamlit, כך שיהיה נגיש לכלל חברי החטיבה מכל מכשיר ובכל זמן.

---

## שלב 1: יצירת מאגר ב-GitHub והעלאת הקוד

1. היכנסו ל-[GitHub](https://github.com) והתחברו לחשבונכם.
2. צרו מאגר חדש (**New repository**):
   * **Repository name:** בחרו שם (למשל: `academic-paper-downloader`).
   * **Public / Private:** מומלץ לבחור ב-**Private** (פרטי) כדי שהקוד ומשאבי האפליקציה יהיו גלויים רק לכם.
   * **Initialize this repository with:** אל תבחרו כלום (השאירו הכל ריק).
   * לחצו על **Create repository**.
3. במחשב שלכם, פתחו את הטרמינל בתיקיית הפרויקט והריצו את הפקודות הבאות לקישור המאגר ודחיפת הקוד:
   ```bash
   git remote add origin https://github.com/USERNAME/REPOSITORY-NAME.git
   git branch -M main
   git push -u origin main
   ```
   *(החליפו את `USERNAME` ו-`REPOSITORY-NAME` בפרטי המאגר שפתחתם).*

---

## שלב 2: פריסת האפליקציה ב-Streamlit Cloud

1. היכנסו לאתר [Streamlit Community Cloud](https://share.streamlit.io) והתחברו באמצעות חשבון ה-GitHub שלכם.
2. לחצו על הכפתור **Create app** (או **Deploy an app**).
3. מלאו את פרטי הפריסה:
   * **Repository:** בחרו את המאגר שזה עתה יצרתם (למשל `academic-paper-downloader`).
   * **Branch:** בחרו ב-`main`.
   * **Main file path:** רשמו `app.py`.
   * **App URL:** תוכלו להתאים אישית את כתובת האתר שלכם (למשל `paper-downloader-mop.streamlit.app`).

---

## שלב 3: הגדרת סיסמת הגישה (Secrets) 🔒

על מנת לאבטח את האפליקציה כדי שלא כל אדם באינטרנט יוכל להשתמש בה, נגדיר את הסיסמה החטיבתית בצורה מאובטחת:

1. במסך הפריסה ב-Streamlit, לחצו על **Advanced settings** (לפני הלחיצה על Deploy, או לאחר מכן דרך תפריט ניהול האפליקציה בכתובת שלכם).
2. בתיבת הטקסט של ה-**Secrets**, הזינו את הסיסמה הרצויה בפורמט הבא:
   ```toml
   password = "הסיסמה_הסודית_שלכם_כאן"
   ```
   *(למשל: `password = "mop_2026"`)*.
3. לחצו על **Save**.
4. לחצו על **Deploy!**

---

## כיצד לעדכן את האפליקציה בעתיד? 🔄

הענן של Streamlit מחובר ישירות ל-GitHub. בכל פעם שתרצו לעדכן את הקוד, להוסיף פיצ'רים או לשנות עיצוב, פשוט בצעו Push רגיל ל-GitHub:
```bash
git add .
git commit -m "הסבר קצר על השינוי"
git push origin main
```
השרת בענן יזהה את השינוי אוטומטית, יתקין מחדש את הספריות הנדרשות, ויעדכן את האתר באוויר בתוך פחות מדקה – ללא צורך בהשבתת השירות!
