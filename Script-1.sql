create schema client;

create table client (
  idClient serial PRIMARY key not null,
  nameClient varchar(20),
  phone varchar(10),
  email varchar(20),
  idTests int,
  idContract int,
  idSales int);

create table sale (
  idSales serial PRIMARY key not null,
  summary double precision,
  status varchar(20)
);

create table contract (
  idContract serial PRIMARY key not null,
  dateStart date,
  dateFinish date
);

create table tests (
  idTests serial PRIMARY key not null,
  nameTest varchar(50),
  description varchar(100),
  idResults int
);

create table review (
  idReview serial PRIMARY key not null,
  dateReview date,
  description varchar(100),
  idClient int
);

create table groupClient (
  idGroup serial PRIMARY key not null,
  visitDate date,
  nameGroup varchar(100),
  idClient int
);

create table results (
  idResults serial PRIMARY key not null,
  dateResult date,
  description varchar(300)
);


ALTER table client
add CONSTRAINT fkclientsale FOREIGN KEY (idSales) REFERENCES Sale (idSales),
add CONSTRAINT fkclientcontract FOREIGN KEY (idContract) REFERENCES contract (idContract),
add CONSTRAINT fkclienttests FOREIGN KEY (idTests) REFERENCES tests (idTests);


ALTER table groupClient
add CONSTRAINT fkgroupClientclient FOREIGN KEY (idClient) REFERENCES Client (idClient);


ALTER table review
add CONSTRAINT fkreviewclient FOREIGN KEY (idClient) REFERENCES Client (idClient);


ALTER table tests
add CONSTRAINT fktestsresults FOREIGN KEY (idResults) REFERENCES results (idResults);

 
INSERT INTO client (nameClient, phone, email)
VALUES
('Client1', '12345678', 'Client1@gmail.com'),
('Client2', '12345677', 'Client2@gmail.com'),
('Client3', '12345676', 'Client3@gmail.com'),
('Client4', '12345675', 'Client4@gmail.com'),
('Client5', '12345674', 'Client5@gmail.com'),
('Client6', '12345673', 'Client6@gmail.com'),
('Client7', '12345672', 'Client7@gmail.com'),
('Client8', '12345671', 'Client8@gmail.com'),
('Client9', '12345670', 'Client9@gmail.com'),
('Client10', '12345669', 'Client10@gmail.com');

select * from client;

INSERT INTO sale (summary, status)
VALUES 
(500.00, 'Активна'),
(1000.00, 'Активна'),
(750.00, 'Использована'),
(200.00, 'Истекла'),
(300.00, 'Активна'),
(800.00, 'Использована'),
(150.00, 'Активна'),
(400.00, 'Использована'),
(100.00, 'Истекла'),
(600.00, 'Активна');

select * from sale;

 
INSERT INTO tests (nameTest, description)
VALUES 
('Тест Рузвельта', 'Тест на суждения и предпочтения .'),
('Тест на определение типа личности', 'Тест, разработанный для измерения психологических предпочтений.'),
('Методика исследования мотивации', 'Тест для выявления личностных мотивов людей.'),
('Вопросник духовного здоровья', 'Тест, использующийся для измерения духовного здоровья человека.'),
('Тест на уровень агрессивности', 'Самооценочный тест на измерение уровня агрессивности личности.'),
('Тест на самооценку', 'Тест, измеряющий уровень самооценки.'),
('Тест о социальном взаимодействии', 'Тест на измерение трудностей в общении и социальном взаимодействии.'),
('Методика исследования эмпатии', 'Тест для измерения уровня эмпатии.'),
('Тест на определение психотипа', 'Тест на измерение психотипа личности и ее характеристик.'),
('Тест на определение стрессоустойчивости', 'Самооценочный тест на выявление уровня стрессоустойчивости.');

select * from tests;

insert into results (dateResult, description)
VALUES 
('2021-05-01', 'Результат теста свидетельствует о высоком уровне стресса.'),
('2021-06-14', 'Тестирование показало высокую склонность к экстраверсии.'),
('2021-07-23', 'Результаты теста говорят о низкой самооценке.'),
('2021-08-05', 'Результаты теста указывают на ярко выраженные симптомы депрессии.'),
('2021-09-10', 'Результаты теста свидетельствуют о наличии страхов и фобий.'),
('2021-10-20', 'Тест показал высокий уровень мотивации к достижению целей.'),
('2021-11-15', 'Результаты теста говорят о ярко выраженной тревожности.'),
('2021-12-02', 'Тестирование указало на высокий уровень интеллектуальной развитости.'),
('2022-01-14', 'Результаты теста свидетельствуют о наличии профессионального выбора.'),
('2022-02-07', 'Тест показал высокий уровень сенсорных ощущений и внимания.');

select * from results;


insert into contract (dateStart, dateFinish)
VALUES 
('2022-01-15', '2022-07-15'),
('2021-11-01', '2022-01-31'),
('2021-08-01', '2022-08-01'),
('2022-02-10', '2022-11-10'),
('2021-04-05', '2022-04-05'),
('2022-03-01', '2023-03-01'),
('2022-05-21', '2022-11-21'),
('2021-09-15', '2022-03-15'),
('2022-04-01', '2022-10-01'),
('2022-06-01', '2023-06-01');

select * from contract;


insert into review (dateReview, description, idClient)
VALUES 
('2022-01-15', 'Очень понравилось общение с психологом, почувствовал себя понимаемым и услышанным.', 1),
('2021-11-01', 'Сначала было страшно обращаться, но психолог помог справиться со страхами и проблемами.', 2),
('2021-08-01', 'Получила прекрасные советы и рекомендации по улучшению психологического состояния.', 3),
('2022-02-10', 'Было непросто признать свои проблемы, но психолог помог найти решение и продвинуться вперед.', 4),
('2021-04-05', 'Спасибо психологу за поддержку и конструктивное общение.', 5),
('2022-03-01', 'Получил много новых знаний и практических навыков по управлению своим эмоциональным состоянием.', 6),
('2022-05-21', 'Психолог умеет слушать, дает полезные рекомендации и не спешит с выводами.', 7),
('2021-09-15', 'Очень благодарен психологу за помощь в решении сложной ситуации на работе.', 8),
('2022-04-01', 'Психологическая помощь очень важна для людей, страдающих стрессом и депрессией.', 9),
('2022-06-01', 'Считаю, что  обратиться к профессионалу - отличный выбор.', 10);


select * from review;

insert into groupClient (visitDate, nameGroup, idClient)
VALUES 
('2022-01-15', 'Групповая терапия для преодоления социальной фобии', 1),
('2021-11-01', 'Терапевтическая группа для снятия стресса и тревожности', 2),
('2021-08-01', 'Групповое обучение техникам медитации и релаксации', 3),
('2022-02-10', 'Групповая терапия для людей, страдающих депрессией', 4),
('2021-04-05', 'Психологический тренинг по управлению конфликтами', 5),
('2022-03-01', 'Терапия для пар, желающих улучшить качество их взаимоотношений', 6),
('2022-05-21', 'Групповая терапия для подростков с проблемами агрессии и нарушений поведения', 7),
('2021-09-15', 'Групповое обучение и тренинги для лидеров и управленцев', 8),
('2022-04-01', 'Терапевтическая группа для людей, переживающих травматические события', 9),
('2022-06-01', 'Групповые занятия для молодых родителей, желающих улучшить навыки взаимодействия со своими детьми', 10);

select * from groupClient;
