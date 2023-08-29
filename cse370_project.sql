-- phpMyAdmin SQL Dump
-- version 5.1.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Apr 23, 2022 at 05:57 PM
-- Server version: 10.4.22-MariaDB
-- PHP Version: 8.1.2

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `cse370_project`
--

-- --------------------------------------------------------

--
-- Table structure for table `admin`
--

CREATE TABLE `admin` (
  `id` varchar(12) NOT NULL,
  `name` varchar(60) NOT NULL,
  `email` varchar(60) NOT NULL,
  `password` varchar(60) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `admin`
--

INSERT INTO `admin` (`id`, `name`, `email`, `password`) VALUES
('A000', 'Shouri', 'saha@gmail.com', '1234'),
('A001', 'Toishi', 'taslima@gmail.com', '456'),
('A002', 'Halim', 'progga@gmail.com', '7575'),
('A003', 'Ateya', 'shuborna@gmail.com', '8989'),
('A004', 'Mahfuz', 'mahfuz@gmail.com', 'www2'),
('A005', 'Anika', 'anika123@yahoo.com', '125');

-- --------------------------------------------------------

--
-- Table structure for table `assesment`
--

CREATE TABLE `assesment` (
  `course` varchar(8) NOT NULL,
  `semester` varchar(12) NOT NULL,
  `type` varchar(20) NOT NULL,
  `deadline` date NOT NULL,
  `description` varchar(300) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `assesment`
--

INSERT INTO `assesment` (`course`, `semester`, `type`, `deadline`, `description`) VALUES
('CSE221', 'Summer2021', 'Assignment01', '2021-09-09', 'All Question needs to be solved'),
('CSE221', 'Summer2021', 'Assignment02', '2021-09-15', 'All Question needs to be solved'),
('CSE221', 'Summer2021', 'Lab3', '2021-09-27', 'Lab task link provided on bux'),
('CSE221', 'Summer2021', 'Quiz1', '2021-09-06', 'Syllabus: chapter 3'),
('CSE221', 'Summer2021', 'Quiz2', '2021-10-06', 'Syllabus: chapter 4'),
('CSE250', 'Fall2021', 'Assignment02', '2021-10-29', 'Chapter 1'),
('CSE250', 'Fall2021', 'Quiz01', '2021-10-01', 'Chapter 1,2,3'),
('CSE251', 'Fall2021', 'Assignment1', '2021-10-03', 'Task 1 and Task 2 on Bux Lecture Video'),
('CSE251', 'Fall2021', 'Assignment2', '2021-10-20', 'Lecture Video 12'),
('CSE331', 'Fall2021', 'Assignment3', '2020-11-15', 'N/A'),
('CSE331', 'Fall2021', 'Quiz3', '2020-12-07', 'Chapter 4&5'),
('CSE370', 'Fall2021', 'LAB1', '2021-11-11', 'SQL Lecture 01'),
('CSE370', 'Fall2021', 'LAB2', '2021-11-20', 'SQL Lecture 02'),
('CSE370', 'Fall2021', 'LAB4', '2020-01-23', 'Rait 12 tar moddhe na dile thedabo'),
('CSE370', 'Fall2021', 'Quiz1', '2021-10-01', 'At 12:01 pm'),
('CSE370', 'Fall2021', 'Quiz2', '2021-11-12', 'Starts at 3 PM || Duration 30 mins'),
('CSE370', 'Fall2021', 'Quiz5', '2021-10-17', 'Will be held');

-- --------------------------------------------------------

--
-- Table structure for table `enrolled_courses`
--

CREATE TABLE `enrolled_courses` (
  `student_id` int(12) NOT NULL,
  `course` varchar(8) NOT NULL,
  `semester` varchar(12) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `enrolled_courses`
--

INSERT INTO `enrolled_courses` (`student_id`, `course`, `semester`) VALUES
(20101300, 'CSE250', 'Fall2021'),
(20101300, 'CSE251', 'Fall2021'),
(20101300, 'CSE331', 'Fall2021'),
(20101349, 'CSE251', 'Fall2021'),
(20101349, 'CSE331', 'Fall2021'),
(20101425, 'CSE251', 'Fall2021'),
(20101425, 'CSE331', 'Fall2021'),
(20101603, 'CSE331', 'Fall2021');

-- --------------------------------------------------------

--
-- Table structure for table `marks`
--

CREATE TABLE `marks` (
  `student_id` int(12) NOT NULL,
  `course` varchar(8) NOT NULL,
  `semester` varchar(12) NOT NULL,
  `type` varchar(20) NOT NULL,
  `total_marks` float(5,2) NOT NULL,
  `achieved_marks` float(5,2) NOT NULL,
  `updated_by` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `marks`
--

INSERT INTO `marks` (`student_id`, `course`, `semester`, `type`, `total_marks`, `achieved_marks`, `updated_by`) VALUES
(20101300, 'CSE331', 'Fall2021', 'Assignment3', 10.00, 10.00, 'S32'),
(20101425, 'CSE251', 'Fall2021', 'Assignment2', 30.00, 30.00, 'AIA'),
(20101425, 'CSE331', 'Fall2021', 'Assignment3', 20.00, 20.00, 'HOS'),
(20101425, 'CSE331', 'Fall2021', 'Quiz3', 30.00, 27.00, 'HOS');

-- --------------------------------------------------------

--
-- Table structure for table `scholarship`
--

CREATE TABLE `scholarship` (
  `student_id` int(12) NOT NULL,
  `credits` int(3) NOT NULL,
  `result` double NOT NULL,
  `description` longtext NOT NULL,
  `status` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `scholarship`
--

INSERT INTO `scholarship` (`student_id`, `credits`, `result`, `description`, `status`) VALUES
(20101300, 66, 3.83, 'Merit Based ', 'DENIED'),
(20101349, 69, 3.99, 'Merit Based ', 'APPROVED'),
(20101425, 66, 4, 'Academic Based', 'NULL'),
(20101603, 66, 4, 'Merit Based ', 'NULL');

-- --------------------------------------------------------

--
-- Table structure for table `student`
--

CREATE TABLE `student` (
  `student_id` int(12) NOT NULL,
  `name` varchar(60) NOT NULL,
  `email` varchar(60) NOT NULL,
  `password` varchar(60) NOT NULL,
  `administer` varchar(12) NOT NULL,
  `status` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `student`
--

INSERT INTO `student` (`student_id`, `name`, `email`, `password`, `administer`, `status`) VALUES
(19201154, 'Labiba', 'labiba.fariha@gsuite.com', '432110', 'A005', NULL),
(19312700, 'Rafid', 'rafid.hasan@gsuite.com', '190', 'A005', NULL),
(20101122, 'Tasnia Jarin', 'tasnia.jarin@gsuite.com', '348', 'A001', NULL),
(20101300, 'Abdul Halim Hosain', 'halim@gmail.com', '7575', 'A004', 'DENIED'),
(20101349, 'shouri', 'shouri.saha.004@gmail.com', '1234', 'Null', 'APPROVED'),
(20101425, 'Ateya', 'stublah1@gmail.com', '111333', 'A000', NULL),
(20101603, 'Taslima Toishi', 'toishi@gmail.com', '4455', 'A004', NULL),
(20101630, 'Ayesha Binte', 'ayesha.binte@gsuite.com', 'wa334', 'A002', NULL),
(20301123, 'Alif Rahman', 'alif.rahman@gsuite.com', 'al554', 'A003', NULL);

-- --------------------------------------------------------

--
-- Table structure for table `ta_modifies`
--

CREATE TABLE `ta_modifies` (
  `teacher_id` varchar(20) NOT NULL,
  `course` varchar(8) NOT NULL,
  `semester` varchar(12) NOT NULL,
  `type` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `ta_modifies`
--

INSERT INTO `ta_modifies` (`teacher_id`, `course`, `semester`, `type`) VALUES
('AIA', 'CSE251', 'Fall2021', 'Assignment1'),
('AIA', 'CSE251', 'Fall2021', 'Assignment2'),
('HOS', 'CSE331', 'Fall2021', 'Assignment3'),
('HOS', 'CSE331', 'Fall2021', 'Quiz3'),
('S32', 'CSE370', 'Fall2021', 'Quiz5');

-- --------------------------------------------------------

--
-- Table structure for table `teacher`
--

CREATE TABLE `teacher` (
  `teacher_id` varchar(20) NOT NULL,
  `name` varchar(60) NOT NULL,
  `email` varchar(60) NOT NULL,
  `password` varchar(60) NOT NULL,
  `appointed_by` varchar(12) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `teacher`
--

INSERT INTO `teacher` (`teacher_id`, `name`, `email`, `password`, `appointed_by`) VALUES
('AIA', 'Anika Islam Apsara', 'anika.islam@g.bracu.ac.bd', '555', 'A004'),
('HOS', 'Hossain Arif', 'hossain.arif@g.bracu.ac.bd', '666', 'A005'),
('S32', 'Ismat', 'ismat@gmail.com', '789', 'A004'),
('S48', 'Akhlaqur Rahman Sabby', 'sabby@gmail.com', '456', 'A004'),
('TAW', 'Tawhid Anwar', 'tawhid@gmail.com', '456', 'A004');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `admin`
--
ALTER TABLE `admin`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `assesment`
--
ALTER TABLE `assesment`
  ADD PRIMARY KEY (`course`,`semester`,`type`);

--
-- Indexes for table `enrolled_courses`
--
ALTER TABLE `enrolled_courses`
  ADD PRIMARY KEY (`student_id`,`course`,`semester`),
  ADD KEY `student_id` (`student_id`,`course`,`semester`),
  ADD KEY `course` (`course`,`semester`);

--
-- Indexes for table `marks`
--
ALTER TABLE `marks`
  ADD PRIMARY KEY (`student_id`,`course`,`semester`,`type`),
  ADD KEY `marks_ibfk_1` (`course`,`semester`,`type`),
  ADD KEY `marks_ibfk_3` (`updated_by`);

--
-- Indexes for table `scholarship`
--
ALTER TABLE `scholarship`
  ADD PRIMARY KEY (`student_id`);

--
-- Indexes for table `student`
--
ALTER TABLE `student`
  ADD PRIMARY KEY (`student_id`),
  ADD KEY `administer` (`administer`);

--
-- Indexes for table `ta_modifies`
--
ALTER TABLE `ta_modifies`
  ADD PRIMARY KEY (`teacher_id`,`course`,`semester`,`type`),
  ADD KEY `ta_modifies_ibfk_1` (`course`,`semester`,`type`);

--
-- Indexes for table `teacher`
--
ALTER TABLE `teacher`
  ADD PRIMARY KEY (`teacher_id`),
  ADD KEY `appointed_by` (`appointed_by`);

--
-- Constraints for dumped tables
--

--
-- Constraints for table `enrolled_courses`
--
ALTER TABLE `enrolled_courses`
  ADD CONSTRAINT `enrolled_courses_ibfk_1` FOREIGN KEY (`course`,`semester`) REFERENCES `assesment` (`course`, `semester`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `enrolled_courses_ibfk_2` FOREIGN KEY (`student_id`) REFERENCES `student` (`student_id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `marks`
--
ALTER TABLE `marks`
  ADD CONSTRAINT `marks_ibfk_1` FOREIGN KEY (`course`,`semester`,`type`) REFERENCES `assesment` (`course`, `semester`, `type`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `marks_ibfk_2` FOREIGN KEY (`student_id`) REFERENCES `student` (`student_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `marks_ibfk_3` FOREIGN KEY (`updated_by`) REFERENCES `teacher` (`teacher_id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `scholarship`
--
ALTER TABLE `scholarship`
  ADD CONSTRAINT `scholarship_ibfk_1` FOREIGN KEY (`student_id`) REFERENCES `student` (`student_id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `ta_modifies`
--
ALTER TABLE `ta_modifies`
  ADD CONSTRAINT `ta_modifies_ibfk_1` FOREIGN KEY (`course`,`semester`,`type`) REFERENCES `assesment` (`course`, `semester`, `type`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `ta_modifies_ibfk_2` FOREIGN KEY (`teacher_id`) REFERENCES `teacher` (`teacher_id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `teacher`
--
ALTER TABLE `teacher`
  ADD CONSTRAINT `teacher_ibfk_1` FOREIGN KEY (`appointed_by`) REFERENCES `admin` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
