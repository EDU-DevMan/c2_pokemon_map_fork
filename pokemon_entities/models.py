from django.db import models  # noqa F401


# your models here
class Pokemon(models.Model):
    """Описание покемона."""
    title = models.CharField(verbose_name='Название покемона по-русски',
                             max_length=200)
    description = models.TextField(verbose_name='Описание покемона',
                                   max_length=255, null=True, blank=True)
    title_en = models.CharField(verbose_name='Название покемона по-английски',
                                max_length=200, null=True, blank=True)
    title_jp = models.CharField(verbose_name='Название покемона по-японски',
                                max_length=200, null=True, blank=True)
    image = models.ImageField(verbose_name='Изображение покемона',
                              upload_to='image/', null=True, blank=True)
    previous_evolution = models.ForeignKey(
        'self', on_delete=models.CASCADE,
        verbose_name='Из кого эволюционирует',
        related_name='next_evolutions',
        null=True, blank=True,)
    next_evolution = models.ForeignKey(
        'self', on_delete=models.CASCADE,
        verbose_name='В кого эволюционирует',
        # related_name='previous_evolution',
        null=True, blank=True,)

    def __str__(self):
        return f'{self.title}'


class PokemonEntity(models.Model):
    """Характеристики покемона."""
    pokemon = models.ForeignKey(Pokemon, verbose_name='Название покемона',
                                on_delete=models.CASCADE)
    lat = models.FloatField(verbose_name='Широта',)

    lon = models.FloatField(verbose_name='Долгота',)

    appeared_at = models.DateTimeField(verbose_name='Дата появления',
                                       null=True, blank=True)
    disappeared_at = models.DateTimeField(verbose_name='Дата исчезновения',
                                          null=True, blank=True)
    level = models.IntegerField(verbose_name='Уровень',
                                null=True, blank=True)
    health = models.IntegerField(verbose_name='Здоровье',
                                 null=True, blank=True)
    strength = models.IntegerField(verbose_name='Атака',
                                   null=True, blank=True)
    defense = models.IntegerField(verbose_name='Защита',
                                  null=True, blank=True)
    stamina = models.IntegerField(verbose_name='Выносливость',
                                  null=True, blank=True)

    def __str__(self):
        return f'{self.pokemon.title}'
