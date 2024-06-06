# CryptoBot

Телеграм бот для отслеживания криптовалют

## Начало работы

Эти инструкции помогут вам скопировать проект и запустить его на вашем локальном компьютере для целей разработки и тестирования.

### Предварительные требования

Перед началом работы убедитесь, что у вас установлены следующие программы:

- [Python 3.12](https://www.python.org/downloads/)
- [pip](https://pip.pypa.io/en/stable/installation/)

### Установка

1. Клонируйте репозиторий проекта:

    ```bash
    git clone https://github.com/Dasifue/CryptoBot
    cd CryptoBot
    ```

2. Создайте виртуальное окружение:

    ```bash
    python3.12 -m venv venv
    ```

3. Активируйте виртуальное окружение:

    - Для Windows:

        ```bash
        .\venv\Scripts\activate
        ```

    - Для MacOS/Linux:

        ```bash
        source venv/bin/activate
        ```

4. Установите зависимости:

    ```bash
    pip install -r requirements.txt
    ```

5. Создайте файл `.env` по примеру `.env.example` и заполните его необходимыми значениями.

    ```bash
    cp .env.example .env
    ```

### Запуск проекта

Для запуска проекта выполните следующую команду:

```bash
python3.12 main.py
