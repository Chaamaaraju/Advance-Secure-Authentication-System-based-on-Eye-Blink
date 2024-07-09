# HeidiSQL Dump 
#
# --------------------------------------------------------
# Host:                 127.0.0.1
# Database:             banking
# Server version:       5.0.37-community-nt
# Server OS:            Win32
# Target-Compatibility: Standard ANSI SQL
# HeidiSQL version:     3.2 Revision: 1129
# --------------------------------------------------------

/*!40100 SET CHARACTER SET latin1;*/
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ANSI';*/
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;*/


#
# Database structure for database 'banking'
#

CREATE DATABASE /*!32312 IF NOT EXISTS*/ "banking" /*!40100 DEFAULT CHARACTER SET latin1 */;

USE "banking";


#
# Table structure for table 'client'
#

CREATE TABLE /*!32312 IF NOT EXISTS*/ "client" (
  "cid" varchar(50) default NULL,
  "name" varchar(50) default NULL,
  "fathername" varchar(50) default NULL,
  "email" varchar(50) default NULL,
  "mobile" varchar(50) default NULL,
  "address" varchar(50) default NULL,
  "city" varchar(50) default NULL,
  "state" varchar(50) default NULL,
  "pnum" varchar(50) default NULL,
  "anum" varchar(50) default NULL
) /*!40100 DEFAULT CHARSET=latin1*/;



#
# Dumping data for table 'client'
#

# (No data found.)



#
# Table structure for table 'login'
#

CREATE TABLE /*!32312 IF NOT EXISTS*/ "login" (
  "cid" varchar(50) default NULL,
  "name" varchar(50) default NULL,
  "pin" varchar(50) default NULL,
  "email" varchar(50) default NULL,
  "mobile" varchar(50) default NULL
) /*!40100 DEFAULT CHARSET=latin1*/;



#
# Dumping data for table 'login'
#

LOCK TABLES "login" WRITE;
/*!40000 ALTER TABLE "login" DISABLE KEYS;*/
REPLACE INTO "login" ("cid", "name", "pin", "email", "mobile") VALUES
	('1111','thirumalai kumar','600015','thirumalaikumarp@gmail.com','9600095045');
/*!40000 ALTER TABLE "login" ENABLE KEYS;*/
UNLOCK TABLES;
/*!40101 SET SQL_MODE=@OLD_SQL_MODE;*/
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;*/
