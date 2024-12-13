from data_utils import sp, get_track_ids, insert_to_gsheet, get_artist_ids

time_ranges = ['short_term', 'medium_term', 'long_term']
sheets = ['songs', 'artists']

for time_period in time_ranges:
    # Fetch user data for the given time range
    top_tracks = sp.current_user_top_tracks(limit=20, offset=0, time_range=time_period)
    top_artists = sp.current_user_top_artists(limit=20, offset=0, time_range=time_period)

    # Extract track and artist IDs
    track_ids = get_track_ids(top_tracks)
    artist_ids = get_artist_ids(top_artists)

    # Insert data into the appropriate sheet
    for sheet in sheets:
        if sheet == 'songs':
            insert_to_gsheet(track_ids, time_period, sheet)
        elif sheet == 'artists':
            insert_to_gsheet(artist_ids, time_period, sheet)
