from rest_framework import serializers


class StoreSerializer(serializers.ModelSerializer):

    class Meta:
        fields = (
            'sudoku',
        )

