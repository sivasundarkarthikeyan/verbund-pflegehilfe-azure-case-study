-- Creating a database --
CREATE DATABASE IF NOT EXISTS VP_LEADS;

-- Selecting the created database --
USE VP_LEADS;

-- Creating a table in the database --
CREATE TABLE IF NOT EXISTS CompanyLeads (
  Id VARCHAR(40) PRIMARY KEY, 
  State integer,
  CreatedDateUtc TIMESTAMP, 
  CancellationRequestDateUtc TIMESTAMP, 
  CancellationDateUtc TIMESTAMP, 
  CancellationRejectionDateUtc TIMESTAMP, 
  UndoCancellationDateUtc TIMESTAMP, 
  CanceledEmployee VARCHAR(255), 
  SoldEmployee VARCHAR(255), 
  UpdatedDateUtc TIMESTAMP
);

-- To import data from a file to the table --
-- Option 1 -  Using Import option on a MySQL Workbench as given below
-- https://dev.mysql.com/doc/workbench/en/wb-admin-export-import-management.html

-- Option 2 - Using the code below

LOAD DATA LOCAL INFILE "{FILEPATH}" IGNORE INTO TABLE CompanyLeads
  FIELDS TERMINATED BY ',' ENCLOSED BY '"'
  LINES TERMINATED BY '\r\n'
  IGNORE 1 LINES
  (Id); 

-- {FILEPATH} needs to be replaced with the complete filepath
-- IGNORE keyword is used to ignore the duplicates based on the column Id
-- Ignoring line 1 which happens to be the header row

