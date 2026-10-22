<?php
header('Content-Type: application/json; charset=utf-8');

$statusData = [
    'system' => 'PHP2Shell Vulnerable Sandbox Target',
    'php_version' => PHP_VERSION,
    'zend_version' => zend_version(),
    'sapi' => php_sapi_name(),
    'memory_limit' => ini_get('memory_limit'),
    'post_max_size' => ini_get('post_max_size'),
    'upload_max_filesize' => ini_get('upload_max_filesize'),
    'session_upload_progress_enabled' => (bool)ini_get('session.upload_progress.enabled'),
    'current_memory_allocated_bytes' => memory_get_usage(true),
    'request_info' => [
        'method' => $_SERVER['REQUEST_METHOD'] ?? 'UNKNOWN',
        'remote_addr' => $_SERVER['REMOTE_ADDR'] ?? 'UNKNOWN',
        'content_type' => $_SERVER['CONTENT_TYPE'] ?? 'none',
        'content_length' => $_SERVER['CONTENT_LENGTH'] ?? 0
    ],
    'server_time' => date('Y-m-d H:i:s')
];

echo json_encode($statusData, JSON_PRETTY_PRINT);
