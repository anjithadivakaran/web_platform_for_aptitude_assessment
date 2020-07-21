# Web Platform for Aptitude Assessment
A research oriented project that helps to understand the underlaying patterns of students interest and predict the stream that the student is interested in.

## Abstract
Understanding a students inherent aptitude is very crucial for an individual as well as an educational organisation. The project aims to create a web application
that enables the students to test their aptitude and generate a report accordingly. The project envisages additional components which can assess students attitude and
interest. Based on students attitude, aptitude and interest the application can point out the right kind of courses for the student. The application will be a web application developed using responsive web development technologies. Registration, answering questions and report viewing is the process flow from client side. Properly tagged and categorised database of questions is the backbone of the framework. The application needs to fetch and map appropriate questions from the database for each user. The application is accessible to only the students who have registered through the portal and they can attend the assessment and view and print the report and edit the profile. A data analytics framework will be developed during the second phase of the project. The set of questions compiled for the application is designed to understand the aptitude, attitude, and interest of a student. The data analytics framework will be used for exploring the underlying trend, patterns, and interconnections in the aptitude, attitude, and interest of a student. The tool is developed using the panda python framework. In the final phase of implementation, the developed tools will be integrated with direct classroom activities with the multimedia content developed by the organization.

## Scope of the project
1. Designed for educational purpose.
2. To study aptitude of student based on the scholastic aptitude of the student.
3. Analysing the pattern and underlying trends based on the student’s interest

## Sprint planning

According to this project, there are mainly two sprints, each one contains five and four user stories respectively.

- **Sprint 1: Assessement Applications**

- **Sprint 2: Evaluation and Data Analysis**

## Assessement Applications
This section of the project allows the registered students to attend the aptitude assessment. The student register through this portal fills the compulsory profile
and logs on to the application. The student can view the assessment report. This application also collects the interests and hobbies of students. The application allows
the instructor to prepare the set of questions. Assigning of questions to the students is done automatically, though the question paper is prepared by the instructor. It
also allows the instructor to manage students and also to edit their own profile. The instructor is registered by the administrator.

<p align = "center"><img align = "center" src = "images/Home.png" width = 600 height = 400/></p>
<p align = "center"><img align = "center" src = "images/signup.png" width = 600 height = 400/></p>

### How the Assessment System works?

All the questions are MCQ. Mainly four types of questions are supported by this application.

1. Normal MCQ questions.
2. Question with image and option
3. Question and option with images.
4. Question and option with images.

<p align = "center"><img align = "center" src = "images/point.png" width = 600 height = 400/></p>

Questions can be from four main sections they are, Science, Commerce, Humanities, and Aptitude. Each question is prepared by the instructor. To prepare the question paper the instructor chooses about fifteen questions from each section. And one question paper contains sixty questions. The questions are given a weightage according to which the category that particular question falls. this weightage is made useful for the evaluation of students assessemnt.It is mandatory for the students to attend all the sixty question. Students need not complete the questions all at once and can continue as per their free time.

## ML Framework for Aptitude Development

### TEXT CORPUS PREPARATION
A corpus is a file that contains all the text either in a single language or in multiple languages. The text corpus is prepared by the instructor. The instructor executes the command for preparation only when a large amount of data gets accumulated in the database. With the help of this data, we can classify the dataset into two: the training set and testing set.
<p align = "center"><img align = "center" src = "images/label.png" width = 600 height = 400/></p>
