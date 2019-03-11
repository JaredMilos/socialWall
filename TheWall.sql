-- MySQL dump 10.13  Distrib 8.0.12, for macos10.13 (x86_64)
--
-- Host: 127.0.0.1    Database: the_wall
-- ------------------------------------------------------
-- Server version	8.0.12

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
 SET NAMES utf8 ;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `messages`
--

DROP TABLE IF EXISTS `messages`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `messages` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `message_text` text,
  `recipient_id` int(11) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `user_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `messages`
--

LOCK TABLES `messages` WRITE;
/*!40000 ALTER TABLE `messages` DISABLE KEYS */;
INSERT INTO `messages` VALUES (2,'Hey Darth!  Messages work now.  I will go to the Dark Side.',3,'2018-09-12 21:29:55',2),(3,'Here is a message to Charles from Lacy!',4,'2018-09-13 01:31:20',5),(5,'You\'ve got mail!',2,'2018-09-13 09:59:17',4),(6,'And you get a message!',3,'2018-09-13 09:59:24',4),(7,'And you get a message!',5,'2018-09-13 09:59:30',4),(8,'Beeeeeeeeeeeeees!',6,'2018-09-13 09:59:38',4),(9,'Wonder Woman, reporting for duty.',2,'2018-09-13 12:12:03',14),(10,'May the Force be with you, Darth.  Drinks on Mustafar?',3,'2018-09-13 12:12:28',14),(11,'Linda Carter, yo.',4,'2018-09-13 12:12:42',14),(12,'Hello Lacy, this is Wonder Woman.',5,'2018-09-13 12:12:52',14);
/*!40000 ALTER TABLE `messages` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `users` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `first_name` varchar(255) DEFAULT NULL,
  `last_name` varchar(255) DEFAULT NULL,
  `email` varchar(255) DEFAULT NULL,
  `password` varchar(255) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `messages_in_inbox` tinyint(4) DEFAULT NULL,
  `messages_in_outbox` tinyint(4) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (2,'Jared','Milos','jaredmilosmusic@gmail.com','$2b$12$Vj1RNwbnLxaqj/HIQ8Yy/.Q54ALjEv9fXcPNRpCqWSjflGkaErpTi','2018-09-12 14:13:57',1,1),(3,'Darth','Vader','darth@vader.com','$2b$12$vy0SyZwqoaglzPm/xFBXP.Zaqiu2k33IuQH0LUf2L4LwClzNiBpc2','2018-09-12 14:20:53',1,0),(4,'Charles','Hollins','charles@hollins.com','$2b$12$BdQmz/MxOtFohPyGnkm8JutxtAhtDyCnQFSXc6/24FzKqe0lt6.ly','2018-09-12 15:25:02',1,1),(5,'Lacy','Milos','singbarefoot@mac.com','$2b$12$bq.NBpNM4rljL7cNElDaCOQgM1BcjsyWLDYtQJItXEwCg2mkRtxJS','2018-09-12 23:43:36',1,1),(6,'Boba','Fett','boba@fett.com','$2b$12$UKnX/fpvYeNxH4JO/ux5oOYmzLGfRdzyBM6RBEahbXkCBnzmJtjYu','2018-09-12 23:54:35',1,0),(7,'Luke','Skywalker','luke@skywalker.com','$2b$12$D2SOwcdhnOKatsBbEnTdL.8agqHofX9FTe9YYPC6x4c3JclE59jJi','2018-09-13 10:00:26',0,0),(11,'Kylo','Ren','kylo@ren.com','$2b$12$PUny13GKyMygrluPgQeAH.vPuuOwg5dPXQcf5MgOhbHOt9fh5kRYe','2018-09-13 10:26:52',0,0),(12,'Han','Solo','han@solo.com','$2b$12$QQSpGFAr.0wkjTgs4q/9X.DKc4gBxEEsGHlL4FqqM.ukJwOqZmYaW','2018-09-13 10:28:41',0,0),(13,'Princess','Leia','princess@leia.com','$2b$12$DJYn9w0z0sRPEjIFP2hRjOiy0yx9uazUkR3aAxIH6.1jtTVKw632W','2018-09-13 10:31:21',0,0),(14,'Wonder','Woman','wonder@woman.com','$2b$12$scb5lDTumVIlgWu0ZgCDIuoPL5rEaOxHWaCNopCkWHGXktJnw2qWi','2018-09-13 12:11:26',0,1);
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2018-09-13 12:14:41
