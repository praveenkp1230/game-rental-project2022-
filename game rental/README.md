# Game Rental

[View the live project here](https://game-rental-python.herokuapp.com/).

---


# Introduction

The following is a stock handling system for a physical game rental service.  It is used by the employee who checks in and out the rentals and adds new games and customers.

[Back to top ⇧](#Hangman)

# Note about the project
Github commits between 93 and 107 were made when it was decided to change the way the app worked.  It used unique dynamically generated ID numbers to identify the customers.  This was a far better approach as it meant different customers with the same details can use the system.

This also allowed to begin making and returning rentals by asking for the customer ID.  This was then used to look up the customer details, which could then be checked with the customer.  This also meant that there was no need for functions to check the customers individual details and far cleaner and usable code.

However, this brought up numerous complications and due to time restrictions it was decided to be scrapped and to revert back to the original code.  Please do see the intended revisions in GitHub commits 93 to 107.

# Features

## Add a customer

The user can add new customers to the customers worksheet.  This hold the cutomers first name, last name, date of birth


## Add a game

New games can be added to the games worksheet, holding information on its title, platform, genre, age restriction and stock.


## Print stock

The entirety of the games worksheet can be printed to the screen.


## Make a rental

When a rental is being made, the user is asked to enter the customers first name, last name, the game title and platform.  Once it has checked that all information has been added, the following takes place:

* The title is checked to see if it is in the games worksheet.  This makes sure it is a game that is currently stocked.

* The stock is checked to see if there are any titles currently in stock.

* The platform the game is on is checked to make sure it is the platform the customer wants.

* The customers first name and last name are looked up in the customers worksheet and checked against the inputed data.

* The customers age is worked out using their date of birth and todays date.

* Their age is checked against the minimum age for the game in the games worksheet.

* A due date for the rental to be returned is calculated by adding 3 days to todays date.

* Stock in the games worksheet is reduced by 1.

* The rentals worksheet is updated with the customers first name, last name, game title, platform and due return date.


## Return a rental
A rental can be booked in once returned.  This asks for the customers first name, last name, game and platform.  The rental is then deleted from the rental worksheet.


## Update fines
The fine column in the rentals worksheet can be updated.  This checks an items due return date against todays date and if the due date is in the past the amount of days late is multiplied by the fine_per_day variable and entered into the fines column.

***

# Features to Implement in the future

## Customer ID
A membership ID number will be used when making a rental and return.  This will allow for customers with the same first and last name to use the service.  This was implemented within commit number 93 and 107.  New customers were automatically assigned a unique ID number when being placed in the customers worksheet.  The user was then prompted to input the customers ID number when making a rental and the specific customer data was then displayed.  This could then be confirmed by the user before proceding.  This allowed for a much more realistic and useable app.  However this feature was discarded due to a lack of time.

## Better validation
The error messages displayed to the user will be improved and try / except statements used to catch incorrect details and other issues.

## Fine awareness
Instead of just inputting fines in the rentals worksheet when the user has selected to do so, this would be carried out automatically and the information printed back to the user.


# Technologies Used

## Main Languages Used

- HTML
- Python



# Testing

Details on site testing can be found [here](TESTING.md).


# Deployment

## How the site was Deployed

The app was deployed to Heroku in the following way:

* All dependencies must be added to the Requirements.txt file.

* Once logged into Heroku, click the Create new app button.

* Enter a unique name for the app, a region and click Create app.

* In the Config Vars section of the Setting tab click Reveal Config Vars.  Name a key "CREDS" and copy and paste the creds.json file into the corresponding Value.  A further key named PORT should be created with the value of 8000.

* Click Add buildpack in the Settings page and select Python and click to save changes.  Repeat for Node.js.

* Click the Deploy tab on the Application Confirmation page and select GitHub for connection method.  Enter the name of the GitHub repository and click Connect.

* Click to Automatically Deploy the app each time the master branch is updated.

* Click Open App within the Application Configuration page to run the program.
 


## How to Fork the Repository

1. Log into [GitHub](https://github.com/login) or [create an account](https://github.com/join).
2. Select the [GitHub Repository](https://github.com/mjjstockman/game-rental).
3. Click "Fork" at the top right of the page.
4. The repository will be copied into your GitHub account.

[Back to top ⇧](#Hangman)

## How to create a Clone using SSH

1. Log into [GitHub](https://github.com/login) or [create an account](https://github.com/join).
2. Select the [GitHub Repository](https://github.com/mjjstockman/game-rental).
3. Click on the Code button.
4. Copy the provided SSH link.
5. Open Terminal.
6. Navigate into the directory you want to clone the repository to.
7. Type git clone and paste the copied URL.

```
$ git clone https://github.com/mjjstockman/hangmangame-rental
```

8. Press **Enter**.


# Credits

Many thanks to the following which were used throughout the creation of this site:


- [Git](https://git-scm.com)
- [GitHub](https://github.com)
- [Gspread Docs](https://docs.gspread.org/en/latest/)
- [Stackoverflow](https://stackoverflow.com/)




## Acknowledgements

- Many thanks to my mentor for guidance.
- Thank you to the Code Institute Slack community for their advice.

