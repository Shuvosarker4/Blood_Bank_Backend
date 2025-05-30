from rest_framework import serializers
from .models import BloodRequest, DonationAcceptance

class BloodRequestSerializer(serializers.ModelSerializer):
    remaining_units = serializers.SerializerMethodField()

    class Meta:
        model = BloodRequest
        fields = [
            'id', 'creator', 'blood_group',
            'units_required', 'units_committed', 'remaining_units',
            'location', 'description', 'status', 'created_at', 'needed_by'
        ]
        read_only_fields = [
            'creator', 'units_committed', 'status',
            'created_at', 'remaining_units'
        ]

    def get_remaining_units(self, obj):
        return obj.remaining_units


class DonationAcceptanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = DonationAcceptance
        fields = ['id', 'request', 'donor', 'accepted_at', 'units_committed']
        read_only_fields = ['donor', 'accepted_at']

    def validate(self, attrs):
        request_obj = attrs.get('request')
        units = attrs.get('units_committed')
        current_user = self.context['request'].user
        if request_obj.creator == current_user:
            raise serializers.ValidationError("You cannot donate to your own blood request.")

        if request_obj.status != 'open':
            raise serializers.ValidationError("This blood request is not open.")

        if units > request_obj.units_required:
            raise serializers.ValidationError("Donated units exceed remaining units needed.")

        return attrs

    def create(self, validated_data):
        validated_data['donor'] = self.context['request'].user
        instance = DonationAcceptance.objects.create(**validated_data)
        request_obj = instance.request
        request_obj.units_committed += instance.units_committed
        request_obj.units_required -= instance.units_committed
        request_obj.units_required = max(request_obj.units_required, 0)
        request_obj.update_status()
        request_obj.save()

        return instance
