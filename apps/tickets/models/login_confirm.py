# -*- coding: utf-8 -*-
#
from django.db import models
from django.utils.translation import ugettext_lazy as _

from .base import Ticket

__all__ = ['LoginConfirmTicket']


class LoginConfirmTicket(Ticket):
    ACTION_APPROVE = 'approve'
    ACTION_REJECT = 'reject'
    ACTION_CHOICES = (
        (ACTION_APPROVE, _('Approve')),
        (ACTION_REJECT, _('Reject')),
    )
    ip = models.GenericIPAddressField(blank=True, null=True)
    city = models.CharField(max_length=16, blank=True, default='')
    action = models.CharField(choices=ACTION_CHOICES, max_length=16, default='', blank=True)

    def create_action_comment(self, action, user):
        action_display = dict(self.ACTION_CHOICES).get(action)
        body = '{} {} {}'.format(user, action_display, _("this order"))
        self.comments.create(body=body, user=user, user_display=str(user))

    def perform_action(self, action, user):
        self.create_action_comment(action, user)
        self.action = action
        self.status = self.STATUS_CLOSED
        self.assignee = user
        self.assignees_display = str(user)
        self.save()