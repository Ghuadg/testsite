from django.shortcuts import render
from .forms import SearchForm
import requests
from bs4 import BeautifulSoup


def search(request):
    form = SearchForm(request.GET or None)
    results = []
    if form.is_valid():
        query = form.cleaned_data['query']
        # Здесь заменяем на поиск на Wildberries
        results = search_wildberries(query)  # Пример поиска на Wildberries
    return render(request, 'search/search.html', {'form': form, 'results': results})


def search_wildberries(query):
    # Формируем URL для поиска на Wildberries
    url = f'https://www.wildberries.ru/catalog/0/search.aspx?search={query}'
    response = requests.get(url)

    # Проверяем статус ответа
    if response.status_code != 200:
        return [{'title': 'Ошибка при запросе', 'price': 'Не удалось получить данные'}]

    soup = BeautifulSoup(response.text, 'html.parser')

    # Находим все блоки с товарами
    items = soup.find_all('div', class_='catalog-item')  # Обновите класс, если он изменится

    results = []
    for item in items:
        # Извлекаем название товара
        title = item.find('span', class_='goods-name').text.strip() if item.find('span',
                                                                                 class_='goods-name') else 'Без названия'

        # Извлекаем цену товара
        price = item.find('span', class_='price').text.strip() if item.find('span',
                                                                            class_='price') else 'Цена не указана'

        # Добавляем найденные данные в список результатов
        results.append({'title': title, 'price': price})

    return results