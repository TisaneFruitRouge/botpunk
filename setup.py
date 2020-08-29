from distutils.core import setup

setup(
  name = 'punkbot',         
  packages = ['PUNKBOT'],   
  version = '0.1',      
  license='MIT',        
  description = 'A bot that solves quizzes for you',   
  author = 'Vincent WENDLING',                   
  author_email = 'vincent.wendling@lilo.org',     
  url = 'https://github.com/TisaneFruitRouge/botpunk',   
  download_url = 'https://github.com/TisaneFruitRouge/botpunk/archive/v_02.tar.gz',    
  keywords = ['BOT', 'QUIZZES', 'JETPUNK'],   
  install_requires=[            
          'selenium',
          'beautifulsoup4',
          'requests',
      ],
  classifiers=[
    'Development Status :: 4 - Beta',      
    'Intended Audience :: Developers',      
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   
    'Programming Language :: Python :: 3.8',
  ],
)
