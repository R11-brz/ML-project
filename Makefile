PYTHON = python3
PIP = pip3
DATA_DIR = data

help:
	@echo "Доступные команды:"
	@echo "  make install - Установить необходимые библиотеки (requests, pandas)"
	@echo "  make parse   - Запустить сбор данных из TMDB"
	@echo "  make clean   - Удалить временные файлы и собранные данные"

install:
	@echo "--- Установка зависимостей ---"
	$(PIP) install requests pandas

parse:
	@echo "--- Запуск парсера ---"
	@mkdir -p $(DATA_DIR)
	$(PYTHON) -m src.parser

clean:
	@echo "--- Очистка ---"
	rm -rf $(DATA_DIR)/*.csv
	rm -rf src/__pycache__
	find . -name "*.pyc" -delete

.PHONY: install parse clean help