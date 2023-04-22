# jetpunk-bot

A bot that completes jetpunk quizzes automatically

## Quickstart

Import the library with:

```python
import BOTPUNK
```

Create the bot with :
```python
my_bot = BOTPUNK.bot.BotPunk(username, password, path_to_chromedriver)
```

then run the bot with :
```python
my_bot.run(lang)
```

Where `lang` is a string containing the languages your want the bot to solve the quizzes for.
As instance `my_bot.run('en-fr-es')` will solve the quizzes for English, French and Spanish

Here's the list to of all languages available :

- 'fr' : french
- 'en' : english		
- 'it' : italian
- 'es' : spanish
- 'de' : german
- 'nl' : dutch
- 'pl' : polish
- 'pt' : portugese
- 'fi' : finnish

**DISCLAIMER :** The bot won't be able to solve perfectly all quizzes. There is some it can't solve at all, and other it'll only be able to solve
partially. (But it's good enough :D )


