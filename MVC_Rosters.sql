-- Create the database
CREATE DATABASE IF NOT EXISTS TransferRosters;
USE TransferRosters;

-- Create Teams table
CREATE TABLE IF NOT EXISTS Teams (
    school VARCHAR(100) PRIMARY KEY,
    mascot VARCHAR(100),
    location VARCHAR(100),
    wins VARCHAR(10),
    losses VARCHAR(10)
);

-- Create Players table
CREATE TABLE IF NOT EXISTS Players (
    Name VARCHAR(100) PRIMARY KEY,
    class VARCHAR(50),
    position VARCHAR(50),
    school VARCHAR(100),
    FOREIGN KEY (school) REFERENCES Teams(school)
);

-- Create Portal table
CREATE TABLE IF NOT EXISTS Portal (
    Name VARCHAR(100) PRIMARY KEY,
    class VARCHAR(50),
    position VARCHAR(50),
    Old_School VARCHAR(100),
    New_School VARCHAR(100)
);
