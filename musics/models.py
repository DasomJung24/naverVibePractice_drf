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

    class Meta:
        db_table = 'artists'
        ordering = ['-id']
        indexes = [
            models.Index(fields=['deleted_at']),
            models.Index(fields=['type']),
        ]

    def __str__(self):
        return f'{self.pk}:{self.name}'


class Album(BaseModel, SoftDeleteModel):
    artist = models.ForeignKey('Artist', on_delete=models.DO_NOTHING, db_constraint=False)
    name = models.CharField('앨범명', max_length=32)
    released_at = models.DateTimeField('발매일')
    description = models.TextField('상세설명', null=True)

    class Meta:
        db_table = 'albums'
        ordering = ['-id']
        indexes = [
            models.Index(fields=['deleted_at']),
            models.Index(fields=['artist']),
        ]

    def __str__(self):
        return f'{self.pk}:{self.name}'


class Song(BaseModel, SoftDeleteModel):
    artist = models.ForeignKey('Artist', on_delete=models.DO_NOTHING, db_constraint=False, null=True)
    album = models.ForeignKey('Album', on_delete=models.DO_NOTHING, db_constraint=False)
    title = models.CharField('제목', max_length=32)
    lyrics = models.TextField('가사', null=True)
    genre = models.ManyToManyField('Genre', null=True, db_constraint=False)

    class Meta:
        db_table = 'songs'
        ordering = ['-id']
        indexes = [
            models.Index(fields=['deleted_at']),
            models.Index(fields=['album']),
            models.Index(fields=['artist']),
        ]

    def __str__(self):
        return f'{self.pk}:{self.title}'


class Genre(BaseModel, SoftDeleteModel):
    name = models.CharField(max_length=32)

    class Meta:
        db_table = 'genres'

    def __str__(self):
        return f'{self.pk}:{self.name}'