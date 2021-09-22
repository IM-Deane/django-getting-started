from django.contrib import admin

from .models import Choice, Question

# Choices are added view Question admin page.
class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3 # default number of choices


class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {"fields": ["question_text"]}),
        ("Date information", {"fields": ["pub_date"], "classes": ["collapse"]}),
    ]
    inlines = [ChoiceInline] # Render choice input fields

    # Class fields displayed as columns
    list_display = ("question_text", "pub_date", "was_published_recently")
    
    list_filter = ["pub_date"] # enable sidebar filter (by date)
    search_fields = ["question_text"] # enable search box


admin.site.register(Question, QuestionAdmin)