from model import Model
from view import View
import time

class Controller:
    def __init__(self):
        self.model = Model()
        self.view = View()

    def run(self):
        while True:
            choice = self.view.show_menu()

            if choice == '1':

                count = self.view.get_generation_count()
                
                self.view.show_message(f"Генерація {count} записів... Це може зайняти час.")
                try:

                    start_time = time.time()
                    

                    self.model.generate_data(count)
                    

                    end_time = time.time()
                    

                    execution_time = end_time - start_time
                    

                    self.view.show_message(f"База успішно перезаписана!")
                    self.view.show_message(f"Час генерації: {execution_time:.2f} сек")
                    
                except Exception as e:
                    self.view.show_error(e)

            elif choice == '2':
                rows, headers = self.model.get_all_tickets()
                self.view.show_table(rows, headers)

            elif choice == '3':
                n, c, t = self.view.get_station_input()
                try:
                    self.model.add_station(n, c, t)
                    self.view.show_message("Станцію додано.")
                except Exception as e:
                    self.view.show_error(f"Помилка вставки: {e}")

            elif choice == '4':
                s_id = self.view.get_delete_id()
                try:

                    self.model.delete_station(s_id)
                    self.view.show_message(f"Станцію {s_id} видалено.")
                except Exception as e:

                    self.view.show_error(e)

            elif choice == '5':
                price, city = self.view.get_search_params()
                if price is not None:
                    start_time = time.time()
                    rows, headers = self.model.search_complex(price, city)
                    end_time = time.time()
                    
                    self.view.show_table(rows, headers)
                    self.view.show_message(f"Час виконання запиту: {(end_time - start_time)*1000:.2f} мс")

            elif choice == '6':
                s_id, name, city, s_type = self.view.get_update_station_input()
                try:
                    self.model.update_station(s_id, name, city, s_type)
                    self.view.show_message(f"Дані станції {s_id} оновлено.")
                except Exception as e:
                    self.view.show_error(f"Помилка оновлення: {e}")

            elif choice == '7':
                s_id, dest, dist = self.view.get_route_input()
                try:
                    self.model.add_route(s_id, dest, dist)
                    self.view.show_message("Маршрут успішно додано!")
                except Exception as e:

                    error_msg = str(e)
                    if "foreign key constraint" in error_msg or "violates foreign key" in error_msg:
                        self.view.show_error(f"Неможливо додати маршрут: Станції з ID={s_id} не існує!")
                        self.view.show_error(f"Технічні деталі: {e}")
                    else:
                        self.view.show_error(f"Інша помилка: {e}")

            elif choice == '0':
                break

if __name__ == "__main__":
    app = Controller()
    app.run()