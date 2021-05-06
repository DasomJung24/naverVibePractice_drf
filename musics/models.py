from django.db import models

from naver_vibe_drf.models import BaseModel, SoftDeleteModel


class Artist(BaseModel, SoftDeleteModel):
    type_choices = (
        ('G', 'group'),
        ('S', 'solo')
    )
    group = models.ForeignKey(
        'self',
        related_name='members',
        null=True,
        on_delete=models.DO_NOTHING,
        db_constraint=False
    )
    name = models.CharField('아티스트명', max_length=128)
    type = models.CharField('아티스트타입', max_length=2, choices=type_choices, default='S')
    debut = models.DateField('데뷔일', null=True)
    thumbnail = models.URLField('썸네일', null=True)
    genre = models.ManyToManyField('Genre')

    class Meta:
        db_table = 'artists'
        ordering = ['-id']
        indexes = [
            models.Index(fields=['deleted_at']),
        ]

    def __str__(self):
        return f'{self.pk}:{self.name}'


class Album(BaseModel, SoftDeleteModel):
    artist = models.ForeignKey('Artist', on_delete=models.DO_NOTHING, db_constraint=False)
    name = models.CharField('앨범명', max_length=32)
    released_at = models.DateTimeField('발매일')
    description = models.TextField('상세설명', null=True)
    image = models.URLField('이미지', null=True)

    class Meta:
        db_table = 'albums'
        ordering = ['-id']
        indexes = [
            models.Index(fields=['deleted_at', 'artist']),
        ]

    def __str__(self):
        return f'{self.pk}:{self.name}'


class Track(BaseModel, SoftDeleteModel):
    artist = models.ForeignKey('Artist', on_delete=models.DO_NOTHING, db_constraint=False, null=True)
    album = models.ForeignKey('Album', on_delete=models.DO_NOTHING, db_constraint=False)
    title = models.CharField('제목', max_length=32)
    lyrics = models.TextField('가사', null=True)
    number = models.PositiveIntegerField('순서')
    represent = models.BooleanField('타이틀곡', default=False)
    play_time = models.CharField('재생시간', max_length=8)
    genre = models.ManyToManyField('Genre', null=True, db_constraint=False)

    class Meta:
        db_table = 'tracks'
        ordering = ['-id']
        indexes = [
            models.Index(fields=['deleted_at', 'artist']),
            models.Index(fields=['album']),
        ]

    def __str__(self):
        return f'{self.pk}:{self.title}'


class Genre(BaseModel, SoftDeleteModel):
    name = models.CharField(max_length=32)

    class Meta:
        db_table = 'genres'

    def __str__(self):
        return f'{self.pk}:{self.name}'
