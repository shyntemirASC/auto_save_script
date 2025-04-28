# Auto Save Script 📋🚀

Скрипт для автоматического сбора последних номеров клиентов с JAICP и загрузки их в список обзвона.

## Требования

- Python 3.11+ (рекомендуется)
- Google Chrome установлен на компьютере

## Установка

1. **Создайте и активируйте виртуальное окружение:**

```bash
python -m venv venv
```

* Для Windows:

```bash
venv\Scripts\activate
```

* Для macOS/Linux:

```bash
source venv/bin/activate
```

2. **Установите зависимости:**

```bash
pip install -r requirements.txt
```

3. **Создайте папку для Excel файлов:**

В корне проекта создайте папку excel, где будут сохраняться созданные Excel-файлы:

```bash
mkdir excel
```

4. **Создайте файл .env:**

В корне проекта создайте файл .env со следующими данными:

```bash
USER_EMAIL=your_email@example.com
USER_PASSWORD=your_password
```

После настройки окружения и зависимостей, для запуска скрипта используйте:

```bash
python main.py
```
