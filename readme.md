# eBook Manager
for me, it is used as pdf manager

## features
- Has tags to manager
- can import and export
  - while new book is import, it should has tags to select
  - while export books, we should zip it
- click it could view the book, and locate the position last read.
- books has status, new(new import and not be open yet), reading, readed, delete, archive
  - delete will remove it, archive will move it to an archive folder and could not read on tags view
  - use sqlite to store the status
- I don't need to comment on the pdf book


---
install packages
``` shell
pip install -r requirements.txt
```

update requirements:
``` shell
pip freeze > requirements.txt
```

pack as onefile exe
``` shell
pyinstaller --onefile main.py
```