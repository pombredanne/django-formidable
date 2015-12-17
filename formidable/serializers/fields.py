# -*- coding: utf-8 -*-
from rest_framework import serializers

from formidable.models import Fieldidable
from formidable.serializers.items import ItemSerializer

BASE_FIELDS = ('label', 'type_id', 'placeholder', 'helptext', 'default',)


class SerializerRegister(dict):

    _instance = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance


def load_serializer(klass):
    SerializerRegister.get_instance()[klass.type_id] = klass
    return klass


class FieldListSerializer(serializers.ListSerializer):

    def __init__(self, *args, **kwargs):
        kwargs['child'] = LazyChildProxy()
        return super(FieldListSerializer, self).__init__(*args, **kwargs)


class FieldidableSerializer(serializers.ModelSerializer):

    type_id = None

    items = ItemSerializer(many=True)

    class Meta:
        model = Fieldidable
        list_serializer_class = FieldListSerializer
        fields = '__all__'


@load_serializer
class TextFieldSerializer(FieldidableSerializer):

    type_id = 'text'

    class Meta(FieldidableSerializer.Meta):
        fields = BASE_FIELDS


@load_serializer
class ParagraphFieldSerializer(TextFieldSerializer):

    type_id = 'paragraph'


@load_serializer
class DropdownFieldSerializer(FieldidableSerializer):

    type_id = 'dropdown'

    class Meta(FieldidableSerializer.Meta):
        fields = BASE_FIELDS + ('items', 'multiple')


@load_serializer
class CheckboxFieldSerializer(FieldidableSerializer):

    type_id = 'checkbox'

    class Meta(FieldidableSerializer.Meta):
        fields = BASE_FIELDS + ('items',)


@load_serializer
class CheckboxesFieldSerializer(FieldidableSerializer):

    type_id = 'checkboxes'

    class Meta(FieldidableSerializer):
        fields = BASE_FIELDS + ('items', 'multiple')


@load_serializer
class RadiosFieldSerializer(FieldidableSerializer):

    type_id = 'radios'

    class Meta(FieldidableSerializer.Meta):
        fields = BASE_FIELDS + ('items', 'multiple')


@load_serializer
class RadiosButtonsFieldSerializer(RadiosFieldSerializer):

    type_id = 'radiosButtons'


@load_serializer
class FileFieldSerializer(FieldidableSerializer):

    type_id = 'file'

    class Meta(FieldidableSerializer.Meta):
        fields = BASE_FIELDS


@load_serializer
class DateFieldSerializer(FieldidableSerializer):

    type_id = 'date'

    class Meta(FieldidableSerializer.Meta):
        fields = BASE_FIELDS


@load_serializer
class EmailFieldSerializer(FieldidableSerializer):

    type_id = 'email'

    class Meta(FieldidableSerializer.Meta):
        fields = BASE_FIELDS


@load_serializer
class NumberFieldSerializer(FieldidableSerializer):

    type_id = 'number'

    class Meta(FieldidableSerializer.Meta):
        fields = BASE_FIELDS


def call_right_serializer_by_instance(meth):

    def _wrapper(self, instance, *args, **kwargs):

        serializer = self.get_right_serializer(instance.type_id)
        meth_name = getattr(serializer, meth.__name__)
        return meth_name(instance, *args, **kwargs)

    return _wrapper


def call_right_serializer_by_attrs(meth):

    def _wrapper(self, attrs, *args, **kwargs):

        serializer = self.get_right_serializer(attrs['type_id'])
        meth_name = getattr(serializer, meth.__name__)
        return meth_name(attrs, *args, **kwargs)

    return _wrapper


def call_all_serializer(meth):

    def _wrapper(self, *args, **kwargs):

        for serializer in self.get_all_serializer():
            meth_name = getattr(serializer, meth.__name__)
            return meth_name(*args, **kwargs)

    return _wrapper


class LazyChildProxy(object):

    def __init__(self):
        register = SerializerRegister.get_instance()
        self.register = {key: value() for key, value in register.iteritems()}

    def get_right_serializer(self, type_id):
        return self.register[type_id]

    def get_all_serializer(self):
        return [serializer for serializer in self.register.values()]

    @call_right_serializer_by_instance
    def to_representation(self, instance):
        pass

    @call_all_serializer
    def bind(self, *args, **kwargs):
        pass

    @call_right_serializer_by_attrs
    def run_validation(self):
        pass
