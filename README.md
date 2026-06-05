# PYdotf
## Менеджер Dot файлов на Python
***
### Описание:
PYdotf - это менеджер ваших dot файлов, который создает симлинк на указанный вами конфиг, а сам конфиг перемещает себе в каталог ~/dotfiles
Создающийся с целью обучения *автоматизации на Python*, может кому понадобится данная программа
***
#### Использование:
```bash
╰─ py py_dotf.py -h 
usage: py_dotf.py [-h] [-c CONFIG] {sync,status,add} ...

PYdotf - A Python implementation of the DOTF file format.

positional arguments:
  {sync,status,add}

options:
  -h, --help           show this help message and exit
  -c, --config CONFIG  Path to the config file.
```
***
#### Аргументы:
1. `add` - добавить конфиг 
```bash
pydotf add ~/.zshrc zsh/.zshrc
# ~/.zshrc -> путь к конфигу который нужно добавить
# zsh/.zshrc -> место для конфига (~/dotfiles/zsh/.zshrc)
```
2. `sync` - сихронизация симлинков 
```bash
pydotf sync
```
3. `status` - статус симлинков
```bash
pydotf status
/home/amnez1a/.zshrc [✓] linked
# linked    ✓
# conflict  !
# broken    ✗
# missing   ?
```
***
#### Конфиг
Для настройки программмы используется конфиг toml, который должен быть в ~/.config/dotf/config.toml
[Образец конфига]() в репозитории
***
Нашли баги, ошибки в коде и прочую на эту тему вещь - **issue**