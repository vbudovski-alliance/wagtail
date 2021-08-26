from django import forms

from wagtail.admin.views.bulk_action import BulkAction
from wagtail.core.models import Page


class DefaultPageForm(forms.Form):
    include_descendants = forms.BooleanField(required=False)


class PageBulkAction(BulkAction):
    model = Page
    object_key = 'page'
    form_class = DefaultPageForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pages_with_no_access'] = [
            {'page': page, 'can_edit': page.permissions_for_user(self.request.user).can_edit()} for page in context['pages_with_no_access']
        ]
        return context

    def get_execution_context(self):
        return {
            'user': self.request.user
        }