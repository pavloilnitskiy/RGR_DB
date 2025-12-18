# RGR_DB
Проектування бази даних та ознайомлення з базовими операціями СУБД PostgreSQL

Концептуальна модель предметної області “Онлайн-платформа для бронювання місць у громадському транспорті.”
В логічній моделі предметної області “Онлайн-платформа для бронювання квитків” виділяються наступні сутності та зв’язки між ними:

Сутність “Вокзал” (Station) з атрибутами: station_id, назва, місто, тип вокзалу;

Сутність “Маршрут” (Route) з атрибутами: route_id, пункт призначення, відстань;

Сутність “Рейс” (Trip) з атрибутами: trip_id, тип транспорту, час відправлення, ціна;

Сутність “Пасажир” (Passenger) з атрибутами: passenger_id, повне ім’я, телефон;

Сутність “Бонус-карта” (BonusCard) з атрибутами: card_id, рівень картки;

Сутність “Квиток” (Ticket) з атрибутами: ticket_id, номер місця, час покупки.

Station(інформація про вокзал)  StationID - унікальний ID вокзалу
Name - назва вокзалу
City - місто
Type - тип вокзалу
Serial (PK)
Charvar(50)
Charvar(50)
Enum

Route(інформація про маршрут)
RouteID - унікальний ID маршруту
StationID - ID вокзалу відправлення
Destination - пункт призначення
Distance - відстань (км)
Serial (PK)
Integer (FK)
Charvar(50)
Integer

Trip(інформація про рейс)
TripID - унікальний ID рейсу
RouteID - ID маршруту
Transport - вид транспорту
Dep_Time - час відправлення
Price - ціна квитка
Serial (PK)
Integer (FK)
Enum
Charvar(20)
Integer

Passenger(інформація про пасажира)
PassengerID - унікальний ID пасажира
Full_Name - ПІБ
Phone - телефон
Serial (PK)
Charvar(50)
Charvar(20)

Ticket(інформація про квиток)
TicketID - унікальний ID квитка
TripID - ID рейсу
PassengerID - ID пасажира
Seat_Number - номер місця
Serial (PK)
Integer (FK)
Integer (FK)
Charvar(10)

BonusCard(бонусна програма)
CardID - ID картки
Level - рівень картки
Serial (PK)
Enum

PassengerCard(зв'язок пасажир-картка)
PassengerID - ID пасажира
CardID - ID картки
Integer (FK)
Integer (FK)

