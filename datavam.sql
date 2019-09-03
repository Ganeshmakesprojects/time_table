drop database db;
create database db;
	
use db;

# ALTER USER 'root'@'localhost' IDENTIFIED BY 'password' PASSWORD EXPIRE NEVER;
# ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY '{NewPassword}';

drop table batch;
drop table professor;
drop table course;
drop table rooms;

create table batch(	
	batchid int not null,
	courseid int not null,
	primary key(batchid, courseid)
	);

create table professor(
	profid int not null,
	profname varchar(10),
	courseid int not null

	);

create table course(	
	courseid int not null,
	coursename varchar(10),
	hours int not null
	);

create table rooms(
	room_no int
	);

insert into batch(batchid, courseid) values
	(1,1),(1,2),(1,3),
	(2,3),(2,4),(2,5),(2,6),
	(3,2),(3,7),(3,5),
	(4,4),(4,8);
	
insert into professor(profid, profname ,courseid ) values
	(1,"P.Bera" ,1),(1, "P.Bera" ,2),(2, "Joy" ,3),(3, "D.Dogra" ,4),
	(4, "S.Saha" ,5),(3, "D.Dogra" ,6),(4, "S.Saha" ,7),(2, "Joy" ,8);

insert into course(courseid, coursename , hours) values
	(1, "DBMS" ,10),(2, "ML" ,8),(3, "DSA" ,4),(4, "CG" ,8),(5, "DS" ,8),(6, "COA" ,4),(7, "CN" ,10),(8, "DAA" ,8);

insert into rooms(room_no) values
	(101),(102),(201),(202);
	
select * from batch;
select * from professor;
select * from course;
select * from rooms;