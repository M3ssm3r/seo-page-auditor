# -*- coding: utf-8 -*-

# Быстрый чекер основных SEO-параметров страницы.
# Помогает не забыть базу.

import requests
from bs4 import BeautifulSoup
import sys
import time

def audit_page(url):
    """Запрашивает URL и проводит аудит."""
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    print(f"\n--- Аудит страницы: {url} ---\n")
    
    try:
        start_time = time.time()
        response = requests.get(url, headers=headers, timeout=10)
        end_time = time.time()
        
        # Проверяем, что страница вообще открылась
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"❌ Не удалось загрузить страницу. Ошибка: {e}")
        return

    soup = BeautifulSoup(response.text, 'html.parser')
    
    # --- НАЧИНАЕМ ПРОВЕРКИ ---

    # 1. Title
    title = soup.find('title')
    if title and title.string:
        title_len = len(title.string)
        print(f"✅ Title: '{title.string.strip()}' ({title_len} симв.)")
        if not (50 < title_len < 70):
            print("   ⚠️ Рекомендуемая длина Title: 50-70 символов.")
    else:
        print("❌ Title не найден!")

    # 2. Description
    description = soup.find('meta', attrs={'name': 'description'})
    if description and description.get('content'):
        desc_len = len(description['content'])
        print(f"✅ Description: '{description['content'].strip()[:70]}...' ({desc_len} симв.)")
        if not (140 < desc_len < 160):
            print("   ⚠️ Рекомендуемая длина Description: 140-160 символов.")
    else:
        print("❌ Description не найден!")

    # 3. H1
    h1s = soup.find_all('h1')
    if len(h1s) == 1:
        print(f"✅ H1: '{h1s[0].get_text(strip=True)}'")
    elif len(h1s) > 1:
        print(f"❌ Найдено несколько тегов H1 ({len(h1s)} шт.). Должен быть только один!")
    else:
        print("❌ H1 не найден!")
        
    # 4. Объем текста
    text_content = soup.get_text()
    word_count = len(text_content.split())
    print(f"✅ Объем текста: примерно {word_count} слов.")
    
    # 5. Скорость загрузки
    load_time = round(end_time - start_time, 2)
    print(f"✅ Скорость ответа сервера: {load_time} сек.")
    if load_time > 1:
        print("   ⚠️ Долговато. Идеальное время ответа < 0.5 сек.")

    print("\n--- Аудит завершен ---")


if __name__ == '__main__':
    # Проверяем, что URL передан в качестве аргумента
    if len(sys.argv) < 2:
        print("Использование: python auditor.py <URL>")
    else:
        target_url = sys.argv[1]
        audit_page(target_url)
