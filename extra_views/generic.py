from django.contrib.contenttypes.generic import generic_inlineformset_factory, BaseGenericInlineFormSet
from extra_views.formsets import BaseInlineFormSetMixin, InlineFormSetView


class BaseGenericInlineFormSetMixin(BaseInlineFormSetMixin):
    """
    Base class for constructing an generic inline formset within a view

    IMPORTANT: Because of a Django bug, initial data doesn't work here.
    """

    ct_field = "content_type"
    ct_fk_field = "object_id"
    formset_class = BaseGenericInlineFormSet

    def get_factory_kwargs(self):
        """
        Returns the keyword arguments for calling the formset factory
        """
        kwargs = super(BaseGenericInlineFormSetMixin, self).get_factory_kwargs()
        del kwargs['fk_name']
        kwargs.update({
            "ct_field": self.ct_field,
            "fk_field": self.ct_fk_field,
        })
        return kwargs

    def get_formset(self):
        """
        Returns the final formset class from the inline formset factory
        """
        result = generic_inlineformset_factory(self.inline_model, **self.get_factory_kwargs())
        return result


class GenericInlineFormSet(BaseGenericInlineFormSetMixin):
    """
    An inline class that provides a way to handle generic inline formsets
    """

    def __init__(self, parent_model, request, instance, view_kwargs=None, view=None):
        self.inline_model = self.model
        self.model = parent_model
        self.request = request
        self.object = instance
        self.kwargs = view_kwargs
        self.view = view


class GenericInlineFormSetView(BaseGenericInlineFormSetMixin, InlineFormSetView):
    """
    A view for displaying a generic inline formset for a queryset belonging to a parent model
    """
