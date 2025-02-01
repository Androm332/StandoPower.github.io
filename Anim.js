async function loadAnimeCatalog() {
    const response = await fetch('anime_data.json');
    const animeList = await response.json();

    const catalog = document.getElementById('anime-list');
    catalog.innerHTML = '';

    animeList.forEach(anime => {
        const animeCard = document.createElement('div');
        animeCard.className = 'anime-card';

        // Создаём изображение
        const img = document.createElement('img');
        img.src = anime.image;
        img.alt = anime.title;
        img.style.cursor = 'pointer'; // Изменяем курсор при наведении
        img.onclick = () => redirectToAnime(encodeURIComponent(anime.title)); // Делаем кликабельным

        // Создаём текстовые элементы
        const title = document.createElement('h3');
        title.textContent = anime.title;

        const description = document.createElement('p');
        description.textContent = anime.description;

        // Добавляем элементы в карточку
        animeCard.appendChild(img);
        animeCard.appendChild(title);
        animeCard.appendChild(description);

        // Добавляем карточку в каталог
        catalog.appendChild(animeCard);
    });
}

// Функция для перехода на страницу аниме
function redirectToAnime(title) {
    window.location.href = `anime_page.html?title=${title}`;
}

// Загрузка каталога при загрузке страницы
window.onload = loadAnimeCatalog;

// Функция поиска
function searchAnime() {
    const query = document.getElementById('search').value.toLowerCase();
    const animeCards = document.querySelectorAll('.anime-card');

    animeCards.forEach(card => {
        const title = card.querySelector('h3').textContent.toLowerCase();
        card.style.display = title.includes(query) ? 'block' : 'none';
    });
}
