from django.db.models import QuerySet
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.template.loader import render_to_string
from django.views.decorators.http import require_POST

from .models import Stream


def _stream_rows() -> str:
    return render_to_string(
        "partial/stream_rows.html", {"streams": Stream.objects.all()}
    )


def stream_list(request: HttpRequest) -> HttpResponse:
    streams: QuerySet = Stream.objects.all()
    return render(request, "studentapp/add_stream.html", {"streams": streams})


def add_stream(request: HttpRequest):
    if request.method != "POST":
        return stream_list(request)

    stream_name = request.POST.get("stream_name", "").strip()
    stream_description = request.POST.get("stream_description", "")
    if not stream_name:
        return JsonResponse({"message": "Stream name should be provided"}, status=400)
    if Stream.objects.filter(name=stream_name).exists():
        return JsonResponse({"message": "Stream already exists"}, status=400)

    Stream.objects.create(name=stream_name, description=stream_description)
    return JsonResponse(
        {"streams": _stream_rows(), "message": "Stream added successfully"},
        status=201,
    )


@require_POST
def edit_stream(request: HttpRequest, id: int):
    stream = get_object_or_404(Stream, pk=id)
    stream_name = request.POST.get("stream_name", "").strip()
    stream_description = request.POST.get("stream_description", "")

    if not stream_name:
        return JsonResponse({"message": "Stream name should be provided"}, status=400)
    if Stream.objects.filter(name=stream_name).exclude(pk=id).exists():
        return JsonResponse({"message": "Stream already exists"}, status=400)

    stream.name = stream_name
    stream.description = stream_description
    stream.save(update_fields=["name", "description"])
    return JsonResponse(
        {"streams": _stream_rows(), "message": "Stream updated successfully"},
        status=200,
    )


@require_POST
def delete_stream(request: HttpRequest, stream_id: int):
    stream = get_object_or_404(Stream, pk=stream_id)
    stream.delete()
    return JsonResponse(
        {"streams": _stream_rows(), "message": "Stream deleted successfully"}
    )
