import psycopg2
from db_config import db_params

class Model:
    def __init__(self):
        self.conn = None
        try:
            self.conn = psycopg2.connect(**db_params)
            self.conn.autocommit = True
        except Exception as e:
            print(f"Помилка підключення: {e}")

    def __del__(self):
        if self.conn:
            self.conn.close()


    def generate_data(self, count_passengers):
        sql = f"""
            TRUNCATE "Ticket", "PassengerCard", "BonusCard", "Trip", "Route", "Passenger", "Station" RESTART IDENTITY CASCADE;
            
            INSERT INTO public."BonusCard" (level) VALUES ('Silver'), ('Gold'), ('Standard');
            
            INSERT INTO public."Station" (name, city, type)
            SELECT 'Вокзал ' || (ARRAY['Центральний', 'Південний', 'Східний'])[floor(random()*3+1)],
                   (ARRAY['Київ', 'Львів', 'Одеса', 'Харків', 'Дніпро', 'Вінниця'])[floor(random()*6+1)],
                   (enum_range(NULL::station_type_enum))[floor(random()*3 + 1)]
            FROM generate_series(1, 50);

            INSERT INTO public."Route" (station_id, destination, distance)
            SELECT s.station_id, (ARRAY['Варшава', 'Берлін', 'Прага', 'Лондон'])[floor(random()*4 + 1)], floor(random() * 2000 + 100)::int
            FROM public."Station" s CROSS JOIN generate_series(1, 4) ORDER BY random() LIMIT 200;

            INSERT INTO public."Trip" (route_id, transport, dep_time, price)
            SELECT r.route_id, (enum_range(NULL::transport_enum))[floor(random()*3 + 1)],
                   lpad(floor(random()*24)::text, 2, '0') || ':' || lpad(floor(random()*60)::text, 2, '0'), floor(random() * 5000 + 200)::int
            FROM public."Route" r CROSS JOIN generate_series(1, 5) ORDER BY random();

            INSERT INTO public."Passenger" (full_name, phone)
            SELECT (ARRAY['Олександр', 'Іван', 'Дмитро', 'Анна', 'Марія'])[floor(random()*5+1)] || ' ' || (ARRAY['Шевченко', 'Бойко', 'Коваль'])[floor(random()*3+1)],
                   '+380' || floor(random()*(999999999-660000000) + 660000000)::text
            FROM generate_series(1, {count_passengers});

            INSERT INTO public."PassengerCard" (passenger_id, card_id)
            SELECT p.passenger_id, c.card_id FROM public."Passenger" p
            CROSS JOIN LATERAL (SELECT card_id FROM public."BonusCard" ORDER BY random() + (p.passenger_id * 0) LIMIT 1) c
            WHERE random() < 0.4; 

            INSERT INTO public."Ticket" (trip_id, passenger_id, seat_number)
            SELECT t.trip_id, p.passenger_id, floor(random()*60 + 1)::text || 'A'
            FROM public."Passenger" p
            CROSS JOIN LATERAL (SELECT trip_id FROM public."Trip" ORDER BY random() + (p.passenger_id * 0) LIMIT 1) t;
        """
        
        with self.conn.cursor() as cur:
            cur.execute(sql)

    def get_all_tickets(self, limit=50):
        query = """
            SELECT t.ticket_id, p.full_name, s.city, r.destination, tr.price, tr.transport
            FROM public."Ticket" t
            JOIN public."Passenger" p ON t.passenger_id = p.passenger_id
            JOIN public."Trip" tr ON t.trip_id = tr.trip_id
            JOIN public."Route" r ON tr.route_id = r.route_id
            JOIN public."Station" s ON r.station_id = s.station_id
            LIMIT %s
        """
        with self.conn.cursor() as cur:
            cur.execute(query, (limit,))
            return cur.fetchall(), [desc[0] for desc in cur.description]

    def add_station(self, name, city, s_type):
        with self.conn.cursor() as cur:
            cur.execute('INSERT INTO public."Station" (name, city, type) VALUES (%s, %s, %s)', (name, city, s_type))

    def delete_station(self, station_id):
        with self.conn.cursor() as cur:

            cur.execute('SELECT count(*) FROM public."Route" WHERE station_id = %s', (station_id,))
            if cur.fetchone()[0] > 0:

                raise Exception(f"Неможливо видалити станцію ID {station_id}: існують пов'язані маршрути!")
            

            cur.execute('DELETE FROM public."Station" WHERE station_id = %s', (station_id,))

    def search_complex(self, min_price, city_part):
        query = """
            SELECT 
                r.destination AS "Напрямок", 
                tr.transport AS "Транспорт", 
                COUNT(t.ticket_id) AS "Продано квитків", 
                ROUND(AVG(tr.price), 2) AS "Середня ціна"
            FROM public."Ticket" t
            JOIN public."Trip" tr ON t.trip_id = tr.trip_id
            JOIN public."Route" r ON tr.route_id = r.route_id
            JOIN public."Station" s ON r.station_id = s.station_id
            WHERE tr.price >= %s AND s.city ILIKE %s
            GROUP BY r.destination, tr.transport
            ORDER BY "Середня ціна" DESC
        """
        with self.conn.cursor() as cur:
            cur.execute(query, (min_price, f'%{city_part}%'))
            return cur.fetchall(), [desc[0] for desc in cur.description]
        

    def update_station(self, station_id, new_name, new_city, new_type):
        query = """
            UPDATE public."Station"
            SET name = %s, city = %s, type = %s
            WHERE station_id = %s
        """
        with self.conn.cursor() as cur:
            cur.execute(query, (new_name, new_city, new_type, station_id))

            if cur.rowcount == 0:
                raise Exception(f"Станції з ID {station_id} не знайдено.")


    def add_route(self, station_id, destination, distance):
        query = """
            INSERT INTO public."Route" (station_id, destination, distance)
            VALUES (%s, %s, %s)
        """
        with self.conn.cursor() as cur:
            cur.execute(query, (station_id, destination, distance))