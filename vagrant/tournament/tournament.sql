-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

Drop Database if exists tournament;
Create Database tournament;
\c tournament;
Create Table players (
  playerId    serial NOT NULL PRIMARY KEY,
  fullname    varchar(48) NOT NULL,
  wins        integer,
  matches     integer
);

