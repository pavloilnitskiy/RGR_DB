class View:
    def show_menu(self):
        print("\n--- ЗАЛІЗНИЧНА КАСА (RGR) ---")
        print("1. Згенерувати базу даних (SQL Random)")
        print("2. Показати квитки (Top 50)")
        print("3. Додати станцію")
        print("4. Видалити станцію (з перевіркою зв'язків)")
        print("5. Пошук рейсів (з таймером)")
        print("6. Редагувати станцію (UPDATE)")
        print("7. Додати маршрут (Тест Foreign Key)")
        print("0. Вихід")
        return input("Ваш вибір: ")

    def get_generation_count(self):
        try:
            count = int(input("Скільки пасажирів/квитків згенерувати? (рекомендовано 1000 - 100000): "))
            return count
        except ValueError:
            print("Введіть коректне ціле число!")
            return 1000 
    
    def show_message(self, msg):
        print(f"\n[INFO]: {msg}")

    def show_error(self, err):
        print(f"\n[ERROR]: {err}")

    def show_table(self, rows, headers):
        if not rows:
            print("Дані відсутні.")
            return

        print(" | ".join([f"{str(h):<15}" for h in headers]))
        print("-" * (18 * len(headers)))
 
        for row in rows:
            print(" | ".join([f"{str(val):<15}" for val in row]))

    def get_station_input(self):
        print("Введіть дані нової станції:")
        name = input("Назва (напр. Вокзал Північний): ")
        city = input("Місто: ")
        type_s = input("Тип (Bus Station, Railway Station, Airport): ")
        return name, city, type_s

    def get_delete_id(self):
        return input("Введіть ID станції для видалення: ")

    def get_search_params(self):
        try:
            price = int(input("Мінімальна ціна квитка: "))
            city = input("Частина назви міста відправлення: ")
            return price, city
        except ValueError:
            print("Ціна має бути числом!")
            return None, None


    def get_update_station_input(self):
        print("--- Редагування станції ---")
        s_id = input("Введіть ID станції, яку треба змінити: ")
        print("Введіть НОВІ дані:")
        name = input("Нова назва: ")
        city = input("Нове місто: ")
        type_s = input("Новий тип (Bus Station, Railway Station, Airport): ")
        return s_id, name, city, type_s

    def get_route_input(self):
        print("--- Новий маршрут ---")
        print("Увага! station_id має існувати в базі Station.")
        s_id = input("Введіть ID станції (FK): ")
        dest = input("Пункт призначення: ")
        dist = int(input("Відстань (км): "))
        return s_id, dest, dist