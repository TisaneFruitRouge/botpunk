# jetpunk-bot
A bot that completes jetpunk quizzes automatically



Create the bot with :

my_bot = JetPunkBot(username, password, pathtochromedriver)

then run it with :

my_bot.run(lang)

where lang is a string containing the languages your want the bot to solve the quizzes in.
As instance my_bot.run('en-fr-es') will solve the quizzes in english, frence and spanish

Here's the list to of all languages available :

'fr' : french
'en' : english		
'it' : italian
'es' : spanish
'de' : german
'nl' : dutch
'pl' : polish
'pt' : portugese
'fi' : finnish

DISCLAIMER : The bot won't be able to solve perfectly all quizzes. There is some it can't solve at all, and other it'll only be able to solve
partially. (But it's good enough :D )


